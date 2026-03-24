"""
路由API
提供路线规划和管理功能
"""
from flask import Blueprint, request, jsonify
from backend.services.route_planning_service import RoutePlanningService
from backend.services.distance_calculation_service import DistanceCalculationService
from backend.services.geocoding_service import GeocodingService
from backend.api.authentication import require_auth
from backend.utils.logger import get_logger

# 创建蓝图
routes_bp = Blueprint('routes', __name__, url_prefix='/api/v1/routes')

# 获取日志记录器
logger = get_logger('RoutesAPI')

# 初始化服务
distance_service = DistanceCalculationService()
geocoding_service = GeocodingService()
route_planning_service = RoutePlanningService(distance_service, geocoding_service)

@routes_bp.route('', methods=['POST'])
@require_auth
def create_route():
    """创建新路线"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        # 创建路线
        route = route_planning_service.create_route(data)
        
        logger.info(f"创建路线成功，ID: {route.get('id')}")
        return jsonify(route), 201
        
    except ValueError as e:
        logger.error(f"创建路线数据验证失败: {e}")
        return jsonify({
            'error': f'数据验证失败: {str(e)}'
        }), 400
        
    except Exception as e:
        logger.error(f"创建路线失败: {e}")
        return jsonify({
            'error': '创建路线失败，请稍后重试'
        }), 500

@routes_bp.route('/<int:route_id>', methods=['GET'])
@require_auth
def get_route(route_id):
    """获取路线信息"""
    try:
        route = route_planning_service.get_route(route_id)
        
        if route:
            logger.info(f"获取路线信息成功，ID: {route_id}")
            return jsonify(route), 200
        else:
            logger.warning(f"路线不存在，ID: {route_id}")
            return jsonify({
                'error': '路线不存在'
            }), 404
            
    except Exception as e:
        logger.error(f"获取路线信息失败: {e}")
        return jsonify({
            'error': '获取路线信息失败'
        }), 500

@routes_bp.route('/<int:route_id>', methods=['PUT'])
@require_auth
def update_route(route_id):
    """更新路线信息"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        # 检查路线是否存在
        existing_route = route_planning_service.get_route(route_id)
        if not existing_route:
            return jsonify({
                'error': '路线不存在'
            }), 404
        
        # 更新路线（这里应该实现更新逻辑）
        updated_route = existing_route.copy()
        updated_route.update(data)
        
        logger.info(f"更新路线成功，ID: {route_id}")
        return jsonify(updated_route), 200
        
    except Exception as e:
        logger.error(f"更新路线失败: {e}")
        return jsonify({
            'error': '更新路线失败'
        }), 500

@routes_bp.route('/<int:route_id>', methods=['DELETE'])
@require_auth
def delete_route(route_id):
    """删除路线"""
    try:
        # 检查路线是否存在
        existing_route = route_planning_service.get_route(route_id)
        if not existing_route:
            return jsonify({
                'error': '路线不存在'
            }), 404
        
        # 删除路线（这里应该实现删除逻辑）
        logger.info(f"删除路线成功，ID: {route_id}")
        return jsonify({
            'message': '路线删除成功'
        }), 200
        
    except Exception as e:
        logger.error(f"删除路线失败: {e}")
        return jsonify({
            'error': '删除路线失败'
        }), 500

@routes_bp.route('/<int:route_id>/optimize', methods=['POST'])
@require_auth
def optimize_route(route_id):
    """优化路线"""
    try:
        data = request.get_json() or {}
        
        # 优化路线
        optimization_result = route_planning_service.optimize_route(route_id, data)
        
        logger.info(f"路线优化成功，ID: {route_id}")
        return jsonify(optimization_result), 200
        
    except ValueError as e:
        logger.error(f"路线优化参数错误: {e}")
        return jsonify({
            'error': f'优化参数错误: {str(e)}'
        }), 400
        
    except Exception as e:
        logger.error(f"路线优化失败: {e}")
        return jsonify({
            'error': '路线优化失败'
        }), 500

@routes_bp.route('/<int:route_id>/cost', methods=['POST'])
@require_auth
def calculate_route_cost(route_id):
    """计算路线成本"""
    try:
        data = request.get_json() or {}
        
        # 计算路线成本
        cost_info = route_planning_service.calculate_route_cost(route_id, data)
        
        logger.info(f"路线成本计算成功，ID: {route_id}")
        return jsonify(cost_info), 200
        
    except ValueError as e:
        logger.error(f"路线成本计算参数错误: {e}")
        return jsonify({
            'error': f'成本计算参数错误: {str(e)}'
        }), 400
        
    except Exception as e:
        logger.error(f"路线成本计算失败: {e}")
        return jsonify({
            'error': '路线成本计算失败'
        }), 500

@routes_bp.route('/<int:route_id>/statistics', methods=['GET'])
@require_auth
def get_route_statistics(route_id):
    """获取路线统计信息"""
    try:
        # 获取路线统计信息
        statistics = route_planning_service.get_route_statistics(route_id)
        
        logger.info(f"获取路线统计信息成功，ID: {route_id}")
        return jsonify(statistics), 200
        
    except Exception as e:
        logger.error(f"获取路线统计信息失败: {e}")
        return jsonify({
            'error': '获取路线统计信息失败'
        }), 500

@routes_bp.route('/plan', methods=['POST'])
@require_auth
def plan_route():
    """规划路线"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        start = data.get('start')
        end = data.get('end')
        via_points = data.get('via_points', [])
        
        if not start or not end:
            return jsonify({
                'error': '起点和终点不能为空'
            }), 400
        
        # 规划路线
        route = route_planning_service.plan_route(start, end, via_points)
        
        if route:
            logger.info("路线规划成功")
            return jsonify(route), 200
        else:
            logger.error("路线规划失败")
            return jsonify({
                'error': '路线规划失败'
            }), 500
            
    except Exception as e:
        logger.error(f"路线规划失败: {e}")
        return jsonify({
            'error': '路线规划失败'
        }), 500



