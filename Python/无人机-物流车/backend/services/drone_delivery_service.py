"""
无人机配送服务
提供无人机配送任务管理功能
"""
from typing import List, Dict, Any, Optional
from backend.models.domain_models import Drone, Task, DeliveryPoint, Warehouse
from backend.services.route_planning_service import RoutePlanningService
from backend.services.distance_calculation_service import DistanceCalculationService
from backend.utils.logger import get_logger

logger = get_logger('DroneDeliveryService')

class DroneDeliveryService:
    """无人机配送服务类"""
    
    def __init__(self, route_planning_service: RoutePlanningService = None,
                 distance_calculation_service: DistanceCalculationService = None):
        """
        初始化无人机配送服务
        
        Args:
            route_planning_service: 路线规划服务
            distance_calculation_service: 距离计算服务
        """
        self.route_planning_service = route_planning_service or RoutePlanningService()
        self.distance_calculation_service = distance_calculation_service or DistanceCalculationService()
        self.available_drones = []
        self.active_deliveries = {}
    
    def create_drone_delivery(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建无人机配送任务
        
        Args:
            data: 配送任务数据
            
        Returns:
            创建的配送任务信息
        """
        try:
            # 解析输入数据
            task_data = data.get('task', {})
            drone_data = data.get('drone', {})
            delivery_points_data = data.get('delivery_points', [])
            
            # 创建任务对象
            task = Task(
                id=task_data.get('id', 0),
                delivery_point_id=task_data['delivery_point_id'],
                warehouse_id=task_data['warehouse_id'],
                quantity=task_data['quantity'],
                priority=task_data.get('priority', 0)
            )
            
            # 创建无人机对象
            drone = Drone(
                id=drone_data.get('id', 0),
                registration_number=drone_data['registration_number'],
                capacity=drone_data['capacity'],
                max_speed=drone_data['max_speed'],
                max_range=drone_data['max_range'],
                battery_capacity=drone_data['battery_capacity']
            )
            
            # 创建配送点对象
            delivery_points = []
            for point_data in delivery_points_data:
                point = DeliveryPoint(
                    id=point_data.get('id', 0),
                    name=point_data['name'],
                    address=point_data['address'],
                    latitude=point_data['latitude'],
                    longitude=point_data['longitude'],
                    demand=point_data.get('demand', 0.0)
                )
                delivery_points.append(point)
            
            # 检查无人机容量
            total_demand = sum(point.demand for point in delivery_points)
            if total_demand > drone.capacity:
                raise ValueError(f"配送需求 {total_demand} 超过无人机容量 {drone.capacity}")
            
            # 计算配送路线
            route_info = self._calculate_delivery_route(drone, delivery_points)
            
            # 创建配送任务信息
            delivery_info = {
                'id': task.id,
                'drone_id': drone.id,
                'drone_registration': drone.registration_number,
                'delivery_points': [point.get_location_info() for point in delivery_points],
                'total_demand': total_demand,
                'route_info': route_info,
                'estimated_duration': self._estimate_delivery_duration(route_info['total_distance'], drone.max_speed),
                'status': 'planned'
            }
            
            # 添加到活跃配送列表
            self.active_deliveries[task.id] = delivery_info
            
            logger.info(f"创建无人机配送任务成功，ID: {task.id}, 无人机: {drone.registration_number}")
            return delivery_info
            
        except Exception as e:
            logger.error(f"创建无人机配送任务失败: {e}")
            raise
    
    def get_drone_delivery(self, drone_delivery_id: int) -> Optional[Dict[str, Any]]:
        """
        获取无人机配送任务信息
        
        Args:
            drone_delivery_id: 配送任务ID
            
        Returns:
            配送任务信息或None
        """
        try:
            delivery_info = self.active_deliveries.get(drone_delivery_id)
            if delivery_info:
                logger.info(f"获取无人机配送任务信息，ID: {drone_delivery_id}")
                return delivery_info
            else:
                logger.warning(f"无人机配送任务不存在，ID: {drone_delivery_id}")
                return None
                
        except Exception as e:
            logger.error(f"获取无人机配送任务失败: {e}")
            return None
    
    def start_delivery(self, drone_delivery_id: int) -> bool:
        """
        开始配送任务
        
        Args:
            drone_delivery_id: 配送任务ID
            
        Returns:
            是否成功开始
        """
        try:
            delivery_info = self.active_deliveries.get(drone_delivery_id)
            if not delivery_info:
                logger.error(f"配送任务不存在，ID: {drone_delivery_id}")
                return False
            
            # 更新状态
            delivery_info['status'] = 'in_progress'
            delivery_info['start_time'] = self._get_current_timestamp()
            
            logger.info(f"开始无人机配送任务，ID: {drone_delivery_id}")
            return True
            
        except Exception as e:
            logger.error(f"开始配送任务失败: {e}")
            return False
    
    def complete_delivery(self, drone_delivery_id: int) -> bool:
        """
        完成配送任务
        
        Args:
            drone_delivery_id: 配送任务ID
            
        Returns:
            是否成功完成
        """
        try:
            delivery_info = self.active_deliveries.get(drone_delivery_id)
            if not delivery_info:
                logger.error(f"配送任务不存在，ID: {drone_delivery_id}")
                return False
            
            # 更新状态
            delivery_info['status'] = 'completed'
            delivery_info['end_time'] = self._get_current_timestamp()
            
            # 计算实际用时
            if 'start_time' in delivery_info:
                actual_duration = delivery_info['end_time'] - delivery_info['start_time']
                delivery_info['actual_duration'] = actual_duration
            
            logger.info(f"完成无人机配送任务，ID: {drone_delivery_id}")
            return True
            
        except Exception as e:
            logger.error(f"完成配送任务失败: {e}")
            return False
    
    def cancel_delivery(self, drone_delivery_id: int, reason: str = "") -> bool:
        """
        取消配送任务
        
        Args:
            drone_delivery_id: 配送任务ID
            reason: 取消原因
            
        Returns:
            是否成功取消
        """
        try:
            delivery_info = self.active_deliveries.get(drone_delivery_id)
            if not delivery_info:
                logger.error(f"配送任务不存在，ID: {drone_delivery_id}")
                return False
            
            # 更新状态
            delivery_info['status'] = 'cancelled'
            delivery_info['cancel_reason'] = reason
            delivery_info['cancel_time'] = self._get_current_timestamp()
            
            logger.info(f"取消无人机配送任务，ID: {drone_delivery_id}, 原因: {reason}")
            return True
            
        except Exception as e:
            logger.error(f"取消配送任务失败: {e}")
            return False
    
    def get_available_drones(self) -> List[Dict[str, Any]]:
        """
        获取可用无人机列表
        
        Returns:
            可用无人机列表
        """
        try:
            # 这里应该从数据库获取可用无人机
            # 暂时返回模拟数据
            available_drones = [
                {
                    'id': 1,
                    'registration_number': 'DRONE001',
                    'capacity': 10.0,
                    'max_speed': 60.0,
                    'max_range': 50.0,
                    'battery_capacity': 100.0,
                    'current_battery': 100.0,
                    'status': 'available'
                },
                {
                    'id': 2,
                    'registration_number': 'DRONE002',
                    'capacity': 15.0,
                    'max_speed': 50.0,
                    'max_range': 40.0,
                    'battery_capacity': 120.0,
                    'current_battery': 85.0,
                    'status': 'available'
                }
            ]
            
            logger.info(f"获取可用无人机列表，数量: {len(available_drones)}")
            return available_drones
            
        except Exception as e:
            logger.error(f"获取可用无人机列表失败: {e}")
            return []
    
    def get_delivery_statistics(self) -> Dict[str, Any]:
        """
        获取配送统计信息
        
        Returns:
            统计信息
        """
        try:
            total_deliveries = len(self.active_deliveries)
            completed_deliveries = sum(1 for d in self.active_deliveries.values() if d['status'] == 'completed')
            in_progress_deliveries = sum(1 for d in self.active_deliveries.values() if d['status'] == 'in_progress')
            cancelled_deliveries = sum(1 for d in self.active_deliveries.values() if d['status'] == 'cancelled')
            
            statistics = {
                'total_deliveries': total_deliveries,
                'completed_deliveries': completed_deliveries,
                'in_progress_deliveries': in_progress_deliveries,
                'cancelled_deliveries': cancelled_deliveries,
                'completion_rate': completed_deliveries / max(total_deliveries, 1) * 100
            }
            
            logger.info(f"获取配送统计信息: {statistics}")
            return statistics
            
        except Exception as e:
            logger.error(f"获取配送统计信息失败: {e}")
            return {}
    
    def _calculate_delivery_route(self, drone: Drone, delivery_points: List[DeliveryPoint]) -> Dict[str, Any]:
        """
        计算配送路线
        
        Args:
            drone: 无人机对象
            delivery_points: 配送点列表
            
        Returns:
            路线信息
        """
        try:
            total_distance = 0.0
            
            # 计算各配送点间的距离
            for i in range(len(delivery_points) - 1):
                distance = delivery_points[i].get_distance_to(delivery_points[i + 1])
                total_distance += distance
            
            # 检查无人机航程
            if total_distance > drone.max_range:
                logger.warning(f"配送距离 {total_distance:.2f}km 超过无人机最大航程 {drone.max_range}km")
            
            route_info = {
                'total_distance': total_distance,
                'delivery_sequence': [point.id for point in delivery_points],
                'is_feasible': total_distance <= drone.max_range
            }
            
            return route_info
            
        except Exception as e:
            logger.error(f"计算配送路线失败: {e}")
            return {'total_distance': 0.0, 'delivery_sequence': [], 'is_feasible': False}
    
    def _estimate_delivery_duration(self, distance: float, max_speed: float) -> float:
        """
        估算配送时间
        
        Args:
            distance: 距离(公里)
            max_speed: 最大速度(公里/小时)
            
        Returns:
            预计时间(小时)
        """
        # 考虑起飞、降落、配送等时间
        base_time = 0.5  # 基础时间(小时)
        travel_time = distance / max_speed
        return base_time + travel_time
    
    def _get_current_timestamp(self) -> float:
        """
        获取当前时间戳
        
        Returns:
            时间戳
        """
        import time
        return time.time()



