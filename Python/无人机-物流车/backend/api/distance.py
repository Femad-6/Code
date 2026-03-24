"""
距离计算API
提供距离计算和地理编码功能
"""
from flask import Blueprint, request, jsonify
from backend.services.distance_calculation_service import DistanceCalculationService
from backend.services.geocoding_service import GeocodingService
from backend.api.authentication import require_auth
from backend.utils.logger import get_logger

# 创建蓝图
distance_bp = Blueprint('distance', __name__, url_prefix='/api/v1')

# 获取日志记录器
logger = get_logger('DistanceAPI')

# 初始化服务
distance_service = DistanceCalculationService()
geocoding_service = GeocodingService()

@distance_bp.route('/distances', methods=['POST'])
@require_auth
def calculate_distance():
    """计算距离"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        # 获取起点和终点
        origin = data.get('origin')
        destination = data.get('destination')
        
        if not origin or not destination:
            return jsonify({
                'error': '起点和终点不能为空'
            }), 400
        
        # 计算距离
        distance = distance_service.calculate_distance(origin, destination)
        
        if distance is not None:
            # 转换为公里
            distance_km = distance / 1000
            
            logger.info(f"距离计算成功: {origin} -> {destination} = {distance_km:.2f}km")
            return jsonify({
                'distance': distance_km,
                'distance_meters': distance,
                'origin': origin,
                'destination': destination
            }), 200
        else:
            logger.error(f"距离计算失败: {origin} -> {destination}")
            return jsonify({
                'error': '距离计算失败'
            }), 500
            
    except Exception as e:
        logger.error(f"距离计算失败: {e}")
        return jsonify({
            'error': '距离计算失败'
        }), 500

@distance_bp.route('/distance-matrix', methods=['POST'])
@require_auth
def calculate_distance_matrix():
    """计算距离矩阵"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        points = data.get('points', [])
        if len(points) < 2:
            return jsonify({
                'error': '至少需要两个点才能计算距离矩阵'
            }), 400
        
        # 计算距离矩阵
        matrix = []
        for i, point1 in enumerate(points):
            row = []
            for j, point2 in enumerate(points):
                if i == j:
                    row.append(0.0)
                else:
                    origin = f"{point1['latitude']},{point1['longitude']}"
                    destination = f"{point2['latitude']},{point2['longitude']}"
                    distance = distance_service.calculate_distance(origin, destination)
                    if distance is not None:
                        row.append(distance / 1000)  # 转换为公里
                    else:
                        row.append(0.0)
            matrix.append(row)
        
        logger.info(f"距离矩阵计算成功，大小: {len(matrix)}x{len(matrix[0])}")
        return jsonify({
            'matrix': matrix,
            'points': points
        }), 200
        
    except Exception as e:
        logger.error(f"距离矩阵计算失败: {e}")
        return jsonify({
            'error': '距离矩阵计算失败'
        }), 500

@distance_bp.route('/geocoding', methods=['POST'])
@require_auth
def geocode():
    """地理编码（地址转坐标）"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        address = data.get('address')
        if not address:
            return jsonify({
                'error': '地址不能为空'
            }), 400
        
        # 地理编码
        result = geocoding_service.geocode(address)
        
        if result:
            logger.info(f"地理编码成功: {address}")
            return jsonify(result), 200
        else:
            logger.error(f"地理编码失败: {address}")
            return jsonify({
                'error': '地理编码失败'
            }), 500
            
    except Exception as e:
        logger.error(f"地理编码失败: {e}")
        return jsonify({
            'error': '地理编码失败'
        }), 500

@distance_bp.route('/reverse-geocoding', methods=['POST'])
@require_auth
def reverse_geocode():
    """逆地理编码（坐标转地址）"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None or longitude is None:
            return jsonify({
                'error': '纬度和经度不能为空'
            }), 400
        
        # 验证坐标范围
        if not geocoding_service.validate_coordinates(latitude, longitude):
            return jsonify({
                'error': '坐标范围无效'
            }), 400
        
        # 逆地理编码
        result = geocoding_service.reverse_geocode(latitude, longitude)
        
        if result:
            logger.info(f"逆地理编码成功: ({latitude}, {longitude})")
            return jsonify(result), 200
        else:
            logger.error(f"逆地理编码失败: ({latitude}, {longitude})")
            return jsonify({
                'error': '逆地理编码失败'
            }), 500
            
    except Exception as e:
        logger.error(f"逆地理编码失败: {e}")
        return jsonify({
            'error': '逆地理编码失败'
        }), 500

@distance_bp.route('/batch-geocoding', methods=['POST'])
@require_auth
def batch_geocode():
    """批量地理编码"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        addresses = data.get('addresses', [])
        if not addresses:
            return jsonify({
                'error': '地址列表不能为空'
            }), 400
        
        if len(addresses) > 100:
            return jsonify({
                'error': '批量地理编码最多支持100个地址'
            }), 400
        
        # 批量地理编码
        results = geocoding_service.batch_geocode(addresses)
        
        success_count = sum(1 for v in results.values() if v is not None)
        
        logger.info(f"批量地理编码完成，成功: {success_count}/{len(addresses)}")
        return jsonify({
            'results': results,
            'total': len(addresses),
            'success': success_count,
            'failed': len(addresses) - success_count
        }), 200
        
    except Exception as e:
        logger.error(f"批量地理编码失败: {e}")
        return jsonify({
            'error': '批量地理编码失败'
        }), 500

@distance_bp.route('/route-distance', methods=['POST'])
@require_auth
def calculate_route_distance():
    """计算路线总距离"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        route_points = data.get('route_points', [])
        if len(route_points) < 2:
            return jsonify({
                'error': '路线至少需要两个点'
            }), 400
        
        # 计算路线总距离
        total_distance = distance_service.calculate_route_distance(route_points)
        
        logger.info(f"路线距离计算成功: {total_distance:.2f}km")
        return jsonify({
            'total_distance': total_distance,
            'route_points': route_points,
            'point_count': len(route_points)
        }), 200
        
    except Exception as e:
        logger.error(f"路线距离计算失败: {e}")
        return jsonify({
            'error': '路线距离计算失败'
        }), 500



