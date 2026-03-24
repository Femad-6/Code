"""
无人机API
提供无人机配送任务管理功能
"""
from flask import Blueprint, request, jsonify
from backend.services.drone_delivery_service import DroneDeliveryService
from backend.services.route_planning_service import RoutePlanningService
from backend.services.distance_calculation_service import DistanceCalculationService
from backend.api.authentication import require_auth
from backend.utils.logger import get_logger

# 创建蓝图
drone_bp = Blueprint('drone', __name__, url_prefix='/api/v1/drone_deliveries')

# 获取日志记录器
logger = get_logger('DroneAPI')

# 初始化服务
distance_service = DistanceCalculationService()
route_planning_service = RoutePlanningService(distance_service)
drone_delivery_service = DroneDeliveryService(route_planning_service, distance_service)

@drone_bp.route('', methods=['POST'])
@require_auth
def create_drone_delivery():
    """创建无人机配送任务"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据不能为空'
            }), 400
        
        # 创建无人机配送任务
        drone_delivery = drone_delivery_service.create_drone_delivery(data)
        
        logger.info(f"创建无人机配送任务成功，ID: {drone_delivery.get('id')}")
        return jsonify(drone_delivery), 201
        
    except ValueError as e:
        logger.error(f"创建无人机配送任务数据验证失败: {e}")
        return jsonify({
            'error': f'数据验证失败: {str(e)}'
        }), 400
        
    except Exception as e:
        logger.error(f"创建无人机配送任务失败: {e}")
        return jsonify({
            'error': '创建无人机配送任务失败，请稍后重试'
        }), 500

@drone_bp.route('/<int:drone_delivery_id>', methods=['GET'])
@require_auth
def get_drone_delivery(drone_delivery_id):
    """获取无人机配送任务信息"""
    try:
        drone_delivery = drone_delivery_service.get_drone_delivery(drone_delivery_id)
        
        if drone_delivery:
            logger.info(f"获取无人机配送任务信息成功，ID: {drone_delivery_id}")
            return jsonify(drone_delivery), 200
        else:
            logger.warning(f"无人机配送任务不存在，ID: {drone_delivery_id}")
            return jsonify({
                'error': '无人机配送任务不存在'
            }), 404
            
    except Exception as e:
        logger.error(f"获取无人机配送任务信息失败: {e}")
        return jsonify({
            'error': '获取无人机配送任务信息失败'
        }), 500

@drone_bp.route('/<int:drone_delivery_id>/start', methods=['POST'])
@require_auth
def start_delivery(drone_delivery_id):
    """开始配送任务"""
    try:
        success = drone_delivery_service.start_delivery(drone_delivery_id)
        
        if success:
            logger.info(f"开始配送任务成功，ID: {drone_delivery_id}")
            return jsonify({
                'message': '配送任务已开始'
            }), 200
        else:
            logger.warning(f"开始配送任务失败，ID: {drone_delivery_id}")
            return jsonify({
                'error': '开始配送任务失败'
            }), 400
            
    except Exception as e:
        logger.error(f"开始配送任务失败: {e}")
        return jsonify({
            'error': '开始配送任务失败'
        }), 500

@drone_bp.route('/<int:drone_delivery_id>/complete', methods=['POST'])
@require_auth
def complete_delivery(drone_delivery_id):
    """完成配送任务"""
    try:
        success = drone_delivery_service.complete_delivery(drone_delivery_id)
        
        if success:
            logger.info(f"完成配送任务成功，ID: {drone_delivery_id}")
            return jsonify({
                'message': '配送任务已完成'
            }), 200
        else:
            logger.warning(f"完成配送任务失败，ID: {drone_delivery_id}")
            return jsonify({
                'error': '完成配送任务失败'
            }), 400
            
    except Exception as e:
        logger.error(f"完成配送任务失败: {e}")
        return jsonify({
            'error': '完成配送任务失败'
        }), 500

@drone_bp.route('/<int:drone_delivery_id>/cancel', methods=['POST'])
@require_auth
def cancel_delivery(drone_delivery_id):
    """取消配送任务"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', '')
        
        success = drone_delivery_service.cancel_delivery(drone_delivery_id, reason)
        
        if success:
            logger.info(f"取消配送任务成功，ID: {drone_delivery_id}")
            return jsonify({
                'message': '配送任务已取消'
            }), 200
        else:
            logger.warning(f"取消配送任务失败，ID: {drone_delivery_id}")
            return jsonify({
                'error': '取消配送任务失败'
            }), 400
            
    except Exception as e:
        logger.error(f"取消配送任务失败: {e}")
        return jsonify({
            'error': '取消配送任务失败'
        }), 500

@drone_bp.route('/available', methods=['GET'])
@require_auth
def get_available_drones():
    """获取可用无人机列表"""
    try:
        available_drones = drone_delivery_service.get_available_drones()
        
        logger.info(f"获取可用无人机列表成功，数量: {len(available_drones)}")
        return jsonify({
            'drones': available_drones,
            'count': len(available_drones)
        }), 200
        
    except Exception as e:
        logger.error(f"获取可用无人机列表失败: {e}")
        return jsonify({
            'error': '获取可用无人机列表失败'
        }), 500

@drone_bp.route('/statistics', methods=['GET'])
@require_auth
def get_delivery_statistics():
    """获取配送统计信息"""
    try:
        statistics = drone_delivery_service.get_delivery_statistics()
        
        logger.info("获取配送统计信息成功")
        return jsonify(statistics), 200
        
    except Exception as e:
        logger.error(f"获取配送统计信息失败: {e}")
        return jsonify({
            'error': '获取配送统计信息失败'
        }), 500

@drone_bp.route('/<int:drone_delivery_id>/status', methods=['GET'])
@require_auth
def get_delivery_status(drone_delivery_id):
    """获取配送任务状态"""
    try:
        drone_delivery = drone_delivery_service.get_drone_delivery(drone_delivery_id)
        
        if drone_delivery:
            status_info = {
                'id': drone_delivery_id,
                'status': drone_delivery.get('status', 'unknown'),
                'start_time': drone_delivery.get('start_time'),
                'end_time': drone_delivery.get('end_time'),
                'estimated_duration': drone_delivery.get('estimated_duration'),
                'actual_duration': drone_delivery.get('actual_duration')
            }
            
            logger.info(f"获取配送任务状态成功，ID: {drone_delivery_id}")
            return jsonify(status_info), 200
        else:
            logger.warning(f"无人机配送任务不存在，ID: {drone_delivery_id}")
            return jsonify({
                'error': '无人机配送任务不存在'
            }), 404
            
    except Exception as e:
        logger.error(f"获取配送任务状态失败: {e}")
        return jsonify({
            'error': '获取配送任务状态失败'
        }), 500



