"""
地理编码服务
提供地址与坐标之间的转换功能
"""
import requests
from typing import Dict, Any, Optional, Tuple
from backend.utils.logger import get_logger

logger = get_logger('GeocodingService')

class GeocodingService:
    """地理编码服务类"""
    
    def __init__(self, api_key: str = None):
        """
        初始化地理编码服务
        
        Args:
            api_key: 地图服务API密钥
        """
        self.api_key = api_key
        self.base_url = "http://api.map.baidu.com/geocoder/v3/"
    
    def geocode(self, address: str) -> Optional[Dict[str, Any]]:
        """
        地址转坐标
        
        Args:
            address: 地址字符串
            
        Returns:
            地理编码结果或None
        """
        if not self.api_key:
            logger.warning("未提供API密钥，返回模拟坐标")
            return self._get_mock_coordinates(address)
        
        try:
            params = {
                "address": address,
                "key": self.api_key,
                "output": "json"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == 0:
                result = data.get("result", {})
                location = result.get("location", {})
                
                geocode_result = {
                    "latitude": location.get("lat"),
                    "longitude": location.get("lng"),
                    "address": address,
                    "formatted_address": result.get("formatted_address", address),
                    "confidence": result.get("confidence", 0),
                    "level": result.get("level", "")
                }
                
                logger.debug(f"地理编码成功: {address} -> ({geocode_result['latitude']}, {geocode_result['longitude']})")
                return geocode_result
            else:
                logger.error(f"地理编码失败: {data.get('info', 'Unknown error')}")
                return self._get_mock_coordinates(address)
                
        except requests.RequestException as e:
            logger.error(f"地理编码API请求失败: {e}")
            return self._get_mock_coordinates(address)
        except Exception as e:
            logger.error(f"地理编码失败: {e}")
            return None
    
    def reverse_geocode(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        """
        坐标转地址
        
        Args:
            latitude: 纬度
            longitude: 经度
            
        Returns:
            逆地理编码结果或None
        """
        if not self.api_key:
            logger.warning("未提供API密钥，返回模拟地址")
            return self._get_mock_address(latitude, longitude)
        
        try:
            params = {
                "location": f"{latitude},{longitude}",
                "key": self.api_key,
                "output": "json"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == 0:
                result = data.get("result", {})
                
                reverse_result = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "address": result.get("formatted_address", ""),
                    "confidence": result.get("confidence", 0),
                    "level": result.get("level", "")
                }
                
                logger.debug(f"逆地理编码成功: ({latitude}, {longitude}) -> {reverse_result['address']}")
                return reverse_result
            else:
                logger.error(f"逆地理编码失败: {data.get('info', 'Unknown error')}")
                return self._get_mock_address(latitude, longitude)
                
        except requests.RequestException as e:
            logger.error(f"逆地理编码API请求失败: {e}")
            return self._get_mock_address(latitude, longitude)
        except Exception as e:
            logger.error(f"逆地理编码失败: {e}")
            return None
    
    def get_location_by_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        根据地址获取坐标
        
        Args:
            address: 地址字符串
            
        Returns:
            坐标元组 (纬度, 经度) 或None
        """
        try:
            result = self.geocode(address)
            if result:
                return (result["latitude"], result["longitude"])
            return None
            
        except Exception as e:
            logger.error(f"获取地址坐标失败: {e}")
            return None
    
    def get_address_by_location(self, latitude: float, longitude: float) -> Optional[str]:
        """
        根据坐标获取地址
        
        Args:
            latitude: 纬度
            longitude: 经度
            
        Returns:
            地址字符串或None
        """
        try:
            result = self.reverse_geocode(latitude, longitude)
            if result:
                return result["address"]
            return None
            
        except Exception as e:
            logger.error(f"获取坐标地址失败: {e}")
            return None
    
    def batch_geocode(self, addresses: list) -> Dict[str, Dict[str, Any]]:
        """
        批量地理编码
        
        Args:
            addresses: 地址列表
            
        Returns:
            地址到坐标的映射字典
        """
        results = {}
        
        for address in addresses:
            try:
                result = self.geocode(address)
                if result:
                    results[address] = result
                else:
                    results[address] = None
                    logger.warning(f"地址地理编码失败: {address}")
            except Exception as e:
                logger.error(f"批量地理编码失败，地址: {address}, 错误: {e}")
                results[address] = None
        
        logger.info(f"批量地理编码完成，成功: {sum(1 for v in results.values() if v is not None)}/{len(addresses)}")
        return results
    
    def validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """
        验证坐标是否有效
        
        Args:
            latitude: 纬度
            longitude: 经度
            
        Returns:
            是否有效
        """
        return (-90 <= latitude <= 90) and (-180 <= longitude <= 180)
    
    def _get_mock_coordinates(self, address: str) -> Dict[str, Any]:
        """
        获取模拟坐标（用于测试或API不可用时）
        
        Args:
            address: 地址
            
        Returns:
            模拟坐标结果
        """
        # 简单的哈希算法生成模拟坐标
        hash_value = hash(address) % 1000000
        
        # 模拟北京地区的坐标
        base_lat = 39.9042
        base_lng = 116.4074
        
        mock_lat = base_lat + (hash_value % 1000 - 500) / 10000
        mock_lng = base_lng + (hash_value % 1000 - 500) / 10000
        
        return {
            "latitude": mock_lat,
            "longitude": mock_lng,
            "address": address,
            "formatted_address": f"模拟地址: {address}",
            "confidence": 0.5,
            "level": "mock"
        }
    
    def _get_mock_address(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        获取模拟地址（用于测试或API不可用时）
        
        Args:
            latitude: 纬度
            longitude: 经度
            
        Returns:
            模拟地址结果
        """
        return {
            "latitude": latitude,
            "longitude": longitude,
            "address": f"模拟地址 ({latitude:.4f}, {longitude:.4f})",
            "confidence": 0.5,
            "level": "mock"
        }



