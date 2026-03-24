"""
Flask应用主文件
无人机-物流车系统后端API服务
"""
from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import config
from backend.utils.logger import get_logger
from backend.api.auth import auth_bp
from backend.api.routes import routes_bp
from backend.api.drone import drone_bp
from backend.api.distance import distance_bp
from backend.services.migration_service import MigrationService

# 获取日志记录器
logger = get_logger('FlaskApp')

def initialize_database(app_config):
    """
    初始化数据库
    
    Args:
        app_config: 应用配置对象
        
    Returns:
        初始化是否成功
    """
    try:
        logger.info("开始数据库初始化检查...")
        
        # 创建迁移服务
        migration_service = MigrationService(app_config.DATABASE_CONFIG)
        
        # 检查当前状态
        status = migration_service.get_migration_status()
        logger.info(f"数据库迁移状态: {status}")
        
        if status['is_up_to_date']:
            logger.info("数据库已是最新版本，无需初始化")
            return True
        
        # 执行迁移到最新版本
        if migration_service.migrate_to_latest():
            logger.info("数据库初始化成功")
            return True
        else:
            logger.error("数据库初始化失败")
            return False
            
    except Exception as e:
        logger.error(f"数据库初始化过程中出错: {e}")
        return False
    finally:
        if 'migration_service' in locals():
            migration_service.close()

def create_app(config_name='default'):
    """
    创建Flask应用实例
    
    Args:
        config_name: 配置名称
        
    Returns:
        Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app_config = config[config_name]
    app.config.from_object(app_config)
    
    # 初始化数据库
    if not initialize_database(app_config):
        logger.error("数据库初始化失败，应用启动中止")
        raise Exception("数据库初始化失败")
    
    # 启用CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(drone_bp)
    app.register_blueprint(distance_bp)
    
    # 错误处理
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"400错误: {error}")
        return jsonify({
            'error': '请求参数错误',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        logger.warning(f"401错误: {error}")
        return jsonify({
            'error': '未授权访问',
            'message': '请提供有效的认证令牌'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        logger.warning(f"403错误: {error}")
        return jsonify({
            'error': '禁止访问',
            'message': '权限不足'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404错误: {error}")
        return jsonify({
            'error': '资源不存在',
            'message': '请求的资源未找到'
        }), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"500错误: {error}")
        return jsonify({
            'error': '服务器内部错误',
            'message': '请稍后重试'
        }), 500
    
    # 健康检查端点
    @app.route('/health', methods=['GET'])
    def health_check():
        """健康检查"""
        return jsonify({
            'status': 'healthy',
            'service': '无人机-物流车系统',
            'version': '1.0.0'
        }), 200
    
    # API信息端点
    @app.route('/api', methods=['GET'])
    def api_info():
        """API信息"""
        return jsonify({
            'name': '无人机-物流车系统API',
            'version': '1.0.0',
            'description': '提供无人机配送和路线规划服务',
            'endpoints': {
                'auth': '/api/auth',
                'routes': '/api/v1/routes',
                'drone_deliveries': '/api/v1/drone_deliveries',
                'distance': '/api/v1/distances',
                'geocoding': '/api/v1/geocoding',
                'database': '/api/v1/database'
            }
        }), 200
    
    # 数据库管理端点
    @app.route('/api/v1/database/status', methods=['GET'])
    def database_status():
        """获取数据库状态"""
        try:
            migration_service = MigrationService(app_config.DATABASE_CONFIG)
            status = migration_service.get_migration_status()
            migration_service.close()
            
            return jsonify({
                'status': 'success',
                'data': status
            }), 200
            
        except Exception as e:
            logger.error(f"获取数据库状态失败: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @app.route('/api/v1/database/migrate', methods=['POST'])
    def database_migrate():
        """执行数据库迁移"""
        try:
            migration_service = MigrationService(app_config.DATABASE_CONFIG)
            
            # 迁移到最新版本
            success = migration_service.migrate_to_latest()
            migration_service.close()
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': '数据库迁移成功'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': '数据库迁移失败'
                }), 500
                
        except Exception as e:
            logger.error(f"数据库迁移失败: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @app.route('/api/v1/database/reset', methods=['POST'])
    def database_reset():
        """重置数据库"""
        try:
            migration_service = MigrationService(app_config.DATABASE_CONFIG)
            
            # 重置数据库
            success = migration_service.reset_database()
            migration_service.close()
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': '数据库重置成功'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': '数据库重置失败'
                }), 500
                
        except Exception as e:
            logger.error(f"数据库重置失败: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    logger.info(f"Flask应用创建成功，配置: {config_name}")
    return app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    logger.info("启动无人机-物流车系统后端服务")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config.get('DEBUG', False)
    )


