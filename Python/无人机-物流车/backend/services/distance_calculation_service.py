"""
距离计算服务
提供距离计算和距离矩阵生成功能
"""
import requests
import math
from typing import List, Dict, Any, Optional, Tuple
from backend.models.domain_models import Location, DeliveryPoint
from backend.utils.logger import get_logger

logger = get_logger('DistanceCalculationService')

class DistanceCalculationService:
    """距离计算服务类"""
    
    def __init__(self, api_key: str = None):
        """
        初始化距离计算服务
        
        Args:
            api_key: 地图服务API密钥
        """
        self.api_key = api_key
        self.base_url = "http://api.map.baidu.com/distance/v3"
    
    def calculate_distance(self, origin: str, destination: str) -> Optional[float]:
        """
        计算两点间距离（使用API）
        
        Args:
            origin: 起点坐标 "纬度,经度"
            destination: 终点坐标 "纬度,经度"
            
        Returns:
            距离(米)或None
        """
        if not self.api_key:
            logger.warning("未提供API密钥，使用Haversine公式计算距离")
            return self._calculate_haversine_distance(origin, destination)
        
        try:
            params = {
                'origins': origin,
                'destinations': destination,
                'output': 'json',
                'ak': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '0':
                distance = data['result'][0]['distance']
                logger.debug(f"API计算距离: {origin} -> {destination} = {distance}m")
                return distance
            else:
                logger.error(f"API计算距离失败: {data.get('status_info', 'Unknown error')}")
                return self._calculate_haversine_distance(origin, destination)
                
        except requests.RequestException as e:
            logger.error(f"API请求失败: {e}")
            return self._calculate_haversine_distance(origin, destination)
        except Exception as e:
            logger.error(f"距离计算失败: {e}")
            return None
    
    def calculate_distances(self, start: Dict[str, Any], end: Dict[str, Any], 
                          via_points: List[Dict[str, Any]]) -> List[float]:
        """
        计算路线各段距离
        
        Args:
            start: 起点信息
            end: 终点信息
            via_points: 途经点列表
            
        Returns:
            距离列表
        """
        try:
            distances = []
            
            # 起点到第一个途经点
            if via_points:
                start_coord = f"{start['latitude']},{start['longitude']}"
                first_via_coord = f"{via_points[0]['latitude']},{via_points[0]['longitude']}"
                distance = self.calculate_distance(start_coord, first_via_coord)
                if distance:
                    distances.append(distance / 1000)  # 转换为公里
                else:
                    distances.append(0.0)
            
            # 途经点之间的距离
            for i in range(len(via_points) - 1):
                coord1 = f"{via_points[i]['latitude']},{via_points[i]['longitude']}"
                coord2 = f"{via_points[i+1]['latitude']},{via_points[i+1]['longitude']}"
                distance = self.calculate_distance(coord1, coord2)
                if distance:
                    distances.append(distance / 1000)  # 转换为公里
                else:
                    distances.append(0.0)
            
            # 最后一个途经点到终点
            if via_points:
                last_via_coord = f"{via_points[-1]['latitude']},{via_points[-1]['longitude']}"
                end_coord = f"{end['latitude']},{end['longitude']}"
                distance = self.calculate_distance(last_via_coord, end_coord)
                if distance:
                    distances.append(distance / 1000)  # 转换为公里
                else:
                    distances.append(0.0)
            
            logger.info(f"计算路线距离完成，共 {len(distances)} 段")
            return distances
            
        except Exception as e:
            logger.error(f"计算路线距离失败: {e}")
            return []
    
    def calculate_distance_matrix(self, points: List[DeliveryPoint]) -> Optional[List[List[float]]]:
        """
        计算距离矩阵
        
        Args:
            points: 配送点列表
            
        Returns:
            距离矩阵或None
        """
        if len(points) < 2:
            logger.warning("配送点数量不足，无法计算距离矩阵")
            return None
        
        try:
            matrix = []
            for i, point1 in enumerate(points):
                row = []
                for j, point2 in enumerate(points):
                    if i == j:
                        row.append(0.0)
                    else:
                        distance = self.get_distance_between_points(point1, point2)
                        row.append(distance)
                matrix.append(row)
            
            logger.info(f"距离矩阵计算完成，大小: {len(matrix)}x{len(matrix[0])}")
            return matrix
            
        except Exception as e:
            logger.error(f"距离矩阵计算失败: {e}")
            return None
    
    def get_distance_between_points(self, point1: DeliveryPoint, point2: DeliveryPoint) -> float:
        """
        计算两个配送点间的距离
        
        Args:
            point1: 配送点1
            point2: 配送点2
            
        Returns:
            距离(公里)
        """
        return point1.get_distance_to(point2)
    
    def get_distance_between_locations(self, location1: Location, location2: Location) -> float:
        """
        计算两个位置间的距离
        
        Args:
            location1: 位置1
            location2: 位置2
            
        Returns:
            距离(公里)
        """
        return location1.distance_to(location2)
    
    def _calculate_haversine_distance(self, origin: str, destination: str) -> float:
        """
        使用Haversine公式计算球面距离
        
        Args:
            origin: 起点坐标 "纬度,经度"
            destination: 终点坐标 "纬度,经度"
            
        Returns:
            距离(米)
        """
        try:
            # 解析坐标
            lat1, lon1 = map(float, origin.split(','))
            lat2, lon2 = map(float, destination.split(','))
            
            # 转换为弧度
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            
            # Haversine公式
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            
            # 地球半径(米)
            r = 6371000
            distance = c * r
            
            logger.debug(f"Haversine计算距离: {origin} -> {destination} = {distance:.2f}m")
            return distance
            
        except Exception as e:
            logger.error(f"Haversine距离计算失败: {e}")
            return 0.0
    
    def calculate_route_distance(self, route_points: List[Tuple[float, float]]) -> float:
        """
        计算路线总距离
        
        Args:
            route_points: 路线点列表 [(纬度, 经度), ...]
            
        Returns:
            总距离(公里)
        """
        if len(route_points) < 2:
            return 0.0
        
        try:
            total_distance = 0.0
            
            for i in range(len(route_points) - 1):
                lat1, lon1 = route_points[i]
                lat2, lon2 = route_points[i + 1]
                
                origin = f"{lat1},{lon1}"
                destination = f"{lat2},{lon2}"
                
                distance = self.calculate_distance(origin, destination)
                if distance:
                    total_distance += distance / 1000  # 转换为公里
            
            logger.info(f"路线总距离计算完成: {total_distance:.2f}km")
            return total_distance
            
        except Exception as e:
            logger.error(f"路线距离计算失败: {e}")
            return 0.0
    
    def find_nearest_point(self, target_point: DeliveryPoint, 
                          candidate_points: List[DeliveryPoint]) -> Optional[DeliveryPoint]:
        """
        找到最近的配送点
        
        Args:
            target_point: 目标点
            candidate_points: 候选点列表
            
        Returns:
            最近的配送点或None
        """
        if not candidate_points:
            return None
        
        try:
            min_distance = float('inf')
            nearest_point = None
            
            for point in candidate_points:
                if point.id != target_point.id:
                    distance = self.get_distance_between_points(target_point, point)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_point = point
            
            logger.info(f"找到最近点: {nearest_point.name if nearest_point else 'None'}, 距离: {min_distance:.2f}km")
            return nearest_point
            
        except Exception as e:
            logger.error(f"查找最近点失败: {e}")
            return None


