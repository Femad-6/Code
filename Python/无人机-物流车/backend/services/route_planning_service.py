"""
路由规划服务
提供路线规划和优化功能
"""
from typing import List, Dict, Any, Optional
from backend.models.domain_models import DeliveryPoint, Warehouse, Route, Location
from backend.services.distance_calculation_service import DistanceCalculationService
from backend.services.geocoding_service import GeocodingService
from backend.utils.logger import get_logger

logger = get_logger('RoutePlanningService')

class RoutePlanningService:
    """路由规划服务类"""
    
    def __init__(self, distance_calculation_service: DistanceCalculationService = None, 
                 geocoding_service: GeocodingService = None):
        """
        初始化路由规划服务
        
        Args:
            distance_calculation_service: 距离计算服务
            geocoding_service: 地理编码服务
        """
        self.distance_calculation_service = distance_calculation_service or DistanceCalculationService()
        self.geocoding_service = geocoding_service or GeocodingService()
    
    def create_route(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新路线
        
        Args:
            data: 路线数据
            
        Returns:
            创建的路线信息
        """
        try:
            # 解析输入数据
            delivery_points_data = data.get('delivery_points', [])
            warehouse_data = data.get('warehouse', {})
            
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
            
            # 创建仓库对象
            warehouse = Warehouse(
                id=warehouse_data.get('id', 0),
                name=warehouse_data['name'],
                address=warehouse_data['address'],
                latitude=warehouse_data['latitude'],
                longitude=warehouse_data['longitude']
            )
            
            # 创建路线
            route = Route(
                id=data.get('id', 0),
                points=delivery_points,
                warehouse=warehouse
            )
            
            # 计算路线距离
            total_distance = route.calculate_total_distance()
            
            # 返回路线信息
            route_info = {
                'id': route.id,
                'delivery_points': [point.get_location_info() for point in delivery_points],
                'warehouse': warehouse.get_location_info(),
                'total_distance': total_distance,
                'estimated_time': self._estimate_travel_time(total_distance),
                'status': 'planned'
            }
            
            logger.info(f"成功创建路线，ID: {route.id}, 总距离: {total_distance:.2f}km")
            return route_info
            
        except Exception as e:
            logger.error(f"创建路线失败: {e}")
            raise
    
    def get_route(self, route_id: int) -> Optional[Dict[str, Any]]:
        """
        获取路线信息
        
        Args:
            route_id: 路线ID
            
        Returns:
            路线信息或None
        """
        try:
            # 这里应该从数据库获取路线信息
            # 暂时返回模拟数据
            logger.info(f"获取路线信息，ID: {route_id}")
            return {
                'id': route_id,
                'delivery_points': [],
                'warehouse': {},
                'total_distance': 0.0,
                'estimated_time': 0.0,
                'status': 'planned'
            }
            
        except Exception as e:
            logger.error(f"获取路线失败: {e}")
            return None
    
    def plan_route(self, start: str, end: str, via_points: List[str]) -> Optional[Dict[str, Any]]:
        """
        规划路线
        
        Args:
            start: 起点地址
            end: 终点地址
            via_points: 途经点列表
            
        Returns:
            路线信息或None
        """
        try:
            # 地理编码
            geocoded_start = self.geocoding_service.geocode(start)
            geocoded_end = self.geocoding_service.geocode(end)
            geocoded_via_points = [self.geocoding_service.geocode(point) for point in via_points]
            
            if not geocoded_start or not geocoded_end or not all(geocoded_via_points):
                logger.error("地理编码失败")
                return None
            
            # 计算距离
            distances = self.distance_calculation_service.calculate_distances(
                geocoded_start, geocoded_end, geocoded_via_points
            )
            
            # 构建路线信息
            route_info = {
                'start': geocoded_start,
                'end': geocoded_end,
                'via_points': geocoded_via_points,
                'distances': distances,
                'total_distance': sum(distances),
                'estimated_time': self._estimate_travel_time(sum(distances))
            }
            
            logger.info(f"路线规划成功，总距离: {route_info['total_distance']:.2f}km")
            return route_info
            
        except Exception as e:
            logger.error(f"路线规划失败: {e}")
            return None
    
    def optimize_route(self, route_id: int, optimization_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        优化路线
        
        Args:
            route_id: 路线ID
            optimization_params: 优化参数
            
        Returns:
            优化结果
        """
        try:
            # 获取路线信息
            route = self.get_route(route_id)
            if not route:
                raise ValueError(f"路线 {route_id} 不存在")
            
            # 这里应该调用优化算法
            # 暂时返回模拟结果
            optimized_route = {
                'id': route_id,
                'original_distance': route.get('total_distance', 0.0),
                'optimized_distance': route.get('total_distance', 0.0) * 0.9,  # 模拟10%优化
                'optimization_ratio': 0.1,
                'status': 'optimized'
            }
            
            logger.info(f"路线优化成功，ID: {route_id}, 优化比例: {optimized_route['optimization_ratio']:.2%}")
            return optimized_route
            
        except Exception as e:
            logger.error(f"路线优化失败: {e}")
            raise
    
    def calculate_route_cost(self, route_id: int, cost_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算路线成本
        
        Args:
            route_id: 路线ID
            cost_params: 成本参数
            
        Returns:
            成本信息
        """
        try:
            route = self.get_route(route_id)
            if not route:
                raise ValueError(f"路线 {route_id} 不存在")
            
            total_distance = route.get('total_distance', 0.0)
            
            # 计算各项成本
            fuel_cost = total_distance * cost_params.get('fuel_cost_per_km', 0.5)
            time_cost = route.get('estimated_time', 0.0) * cost_params.get('time_cost_per_hour', 50)
            maintenance_cost = total_distance * cost_params.get('maintenance_cost_per_km', 0.1)
            
            total_cost = fuel_cost + time_cost + maintenance_cost
            
            cost_info = {
                'route_id': route_id,
                'total_distance': total_distance,
                'fuel_cost': fuel_cost,
                'time_cost': time_cost,
                'maintenance_cost': maintenance_cost,
                'total_cost': total_cost
            }
            
            logger.info(f"路线成本计算完成，ID: {route_id}, 总成本: {total_cost:.2f}")
            return cost_info
            
        except Exception as e:
            logger.error(f"路线成本计算失败: {e}")
            raise
    
    def _estimate_travel_time(self, distance: float, average_speed: float = 50.0) -> float:
        """
        估算旅行时间
        
        Args:
            distance: 距离(公里)
            average_speed: 平均速度(公里/小时)
            
        Returns:
            旅行时间(小时)
        """
        return distance / average_speed
    
    def get_route_statistics(self, route_id: int) -> Dict[str, Any]:
        """
        获取路线统计信息
        
        Args:
            route_id: 路线ID
            
        Returns:
            统计信息
        """
        try:
            route = self.get_route(route_id)
            if not route:
                raise ValueError(f"路线 {route_id} 不存在")
            
            delivery_points = route.get('delivery_points', [])
            
            statistics = {
                'route_id': route_id,
                'total_delivery_points': len(delivery_points),
                'total_distance': route.get('total_distance', 0.0),
                'estimated_time': route.get('estimated_time', 0.0),
                'average_distance_per_point': route.get('total_distance', 0.0) / max(len(delivery_points), 1),
                'status': route.get('status', 'unknown')
            }
            
            logger.info(f"获取路线统计信息，ID: {route_id}")
            return statistics
            
        except Exception as e:
            logger.error(f"获取路线统计信息失败: {e}")
            raise



