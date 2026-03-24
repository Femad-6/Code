"""
认证API路由
提供用户注册、登录等认证功能
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.request_models import UserRequest, LoginRequest
from backend.models.response_models import AuthResponse, ErrorResponse
from backend.data_access.database_connector import DatabaseConnector
from backend.utils.logger import get_logger
from backend.config import config

# 创建蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 获取日志记录器
logger = get_logger('AuthAPI')

# 初始化数据库连接
db_connector = DatabaseConnector(config['default'].DATABASE_CONFIG)

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        user_data = request.get_json()
        if not user_data:
            return jsonify(ErrorResponse(
                success=False, 
                message="请求数据不能为空"
            ).response), 400
        
        # 验证请求数据
        user_request = UserRequest(**user_data)
        
        # 检查用户名是否已存在
        existing_user = db_connector.fetch_one(
            "SELECT id FROM users WHERE username = %s", 
            (user_request.username,)
        )
        
        if existing_user:
            return jsonify(ErrorResponse(
                success=False, 
                message="用户名已存在"
            ).response), 400
        
        # 加密密码
        hashed_password = generate_password_hash(user_request.password)
        
        # 插入新用户
        user_id = db_connector.insert_and_get_id(
            "INSERT INTO users (username, password, created_at) VALUES (%s, %s, NOW())",
            (user_request.username, hashed_password)
        )
        
        logger.info(f"用户注册成功: {user_request.username}, ID: {user_id}")
        
        return jsonify(AuthResponse(
            success=True, 
            message="用户注册成功"
        ).response), 201
        
    except ValueError as e:
        logger.error(f"用户注册数据验证失败: {e}")
        return jsonify(ErrorResponse(
            success=False, 
            message=f"数据验证失败: {str(e)}"
        ).response), 400
        
    except Exception as e:
        logger.error(f"用户注册失败: {e}")
        return jsonify(ErrorResponse(
            success=False, 
            message="注册失败，请稍后重试"
        ).response), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        login_data = request.get_json()
        if not login_data:
            return jsonify(ErrorResponse(
                success=False, 
                message="请求数据不能为空"
            ).response), 400
        
        # 验证请求数据
        login_request = LoginRequest(**login_data)
        
        # 查询用户
        user = db_connector.fetch_one(
            "SELECT id, username, password FROM users WHERE username = %s", 
            (login_request.username,)
        )
        
        if not user:
            return jsonify(ErrorResponse(
                success=False, 
                message="用户名或密码错误"
            ).response), 401
        
        # 验证密码
        if not check_password_hash(user['password'], login_request.password):
            return jsonify(ErrorResponse(
                success=False, 
                message="用户名或密码错误"
            ).response), 401
        
        # 生成令牌（简化版本，实际应用中应使用JWT）
        token = generate_password_hash(f"{user['username']}_{user['id']}")
        
        # 更新最后登录时间
        db_connector.execute_query(
            "UPDATE users SET last_login = NOW() WHERE id = %s",
            (user['id'],)
        )
        
        logger.info(f"用户登录成功: {user['username']}, ID: {user['id']}")
        
        return jsonify(AuthResponse(
            success=True, 
            message="登录成功",
            token=token
        ).response), 200
        
    except ValueError as e:
        logger.error(f"用户登录数据验证失败: {e}")
        return jsonify(ErrorResponse(
            success=False, 
            message=f"数据验证失败: {str(e)}"
        ).response), 400
        
    except Exception as e:
        logger.error(f"用户登录失败: {e}")
        return jsonify(ErrorResponse(
            success=False, 
            message="登录失败，请稍后重试"
        ).response), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    try:
        # 这里可以添加令牌失效逻辑
        logger.info("用户登出")
        
        return jsonify(AuthResponse(
            success=True, 
            message="登出成功"
        ).response), 200
        
    except Exception as e:
        logger.error(f"用户登出失败: {e}")
        return jsonify(ErrorResponse(
            success=False, 
            message="登出失败"
        ).response), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """验证令牌"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify(ErrorResponse(
                success=False, 
                message="缺少认证令牌"
            ).response), 401
        
        token = auth_header.split(' ')[1]
        
        # 这里应该验证令牌的有效性
        # 简化版本，实际应用中应使用JWT验证
        
        logger.info("令牌验证成功")
        
        return jsonify(AuthResponse(
            success=True, 
            message="令牌有效"
        ).response), 200
        
    except Exception as e:
        logger.error(f"令牌验证失败: {e}")
        return jsonify(ErrorResponse(
            success=False, 
            message="令牌无效"
        ).response), 401



