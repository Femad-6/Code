"""
认证装饰器和工具函数
提供API认证功能
"""
from functools import wraps
from flask import request, jsonify
from backend.models.response_models import ErrorResponse
from backend.utils.logger import get_logger

logger = get_logger('Authentication')

def require_auth(f):
    """
    认证装饰器
    验证请求是否包含有效的认证令牌
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # 获取认证头
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                logger.warning("请求缺少认证头")
                return jsonify(ErrorResponse(
                    success=False,
                    message="缺少认证令牌"
                ).response), 401
            
            # 检查Bearer令牌格式
            if not auth_header.startswith('Bearer '):
                logger.warning("认证令牌格式错误")
                return jsonify(ErrorResponse(
                    success=False,
                    message="认证令牌格式错误"
                ).response), 401
            
            # 提取令牌
            token = auth_header.split(' ')[1]
            
            if not token:
                logger.warning("认证令牌为空")
                return jsonify(ErrorResponse(
                    success=False,
                    message="认证令牌为空"
                ).response), 401
            
            # 验证令牌（简化版本）
            if not _validate_token(token):
                logger.warning(f"认证令牌无效: {token[:10]}...")
                return jsonify(ErrorResponse(
                    success=False,
                    message="认证令牌无效"
                ).response), 401
            
            # 将用户信息添加到请求上下文
            user_info = _get_user_info_from_token(token)
            request.current_user = user_info
            
            logger.debug(f"用户认证成功: {user_info.get('username', 'unknown')}")
            return f(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"认证过程中发生错误: {e}")
            return jsonify(ErrorResponse(
                success=False,
                message="认证失败"
            ).response), 500
    
    return decorated_function

def require_admin(f):
    """
    管理员权限装饰器
    验证用户是否具有管理员权限
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # 首先进行基本认证
            auth_result = require_auth(f)(*args, **kwargs)
            
            # 如果认证失败，直接返回
            if isinstance(auth_result, tuple) and auth_result[1] != 200:
                return auth_result
            
            # 检查管理员权限
            user_info = getattr(request, 'current_user', None)
            if not user_info or not user_info.get('is_admin', False):
                logger.warning(f"用户 {user_info.get('username', 'unknown')} 尝试访问管理员功能")
                return jsonify(ErrorResponse(
                    success=False,
                    message="需要管理员权限"
                ).response), 403
            
            logger.debug(f"管理员权限验证成功: {user_info.get('username')}")
            return f(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"管理员权限验证过程中发生错误: {e}")
            return jsonify(ErrorResponse(
                success=False,
                message="权限验证失败"
            ).response), 500
    
    return decorated_function

def _validate_token(token: str) -> bool:
    """
    验证令牌有效性
    
    Args:
        token: 认证令牌
        
    Returns:
        是否有效
    """
    try:
        # 简化版本：检查令牌长度和格式
        # 实际应用中应使用JWT验证
        if len(token) < 10:
            return False
        
        # 这里可以添加更复杂的令牌验证逻辑
        # 例如：检查令牌是否在数据库中，是否过期等
        
        return True
        
    except Exception as e:
        logger.error(f"令牌验证失败: {e}")
        return False

def _get_user_info_from_token(token: str) -> dict:
    """
    从令牌中获取用户信息
    
    Args:
        token: 认证令牌
        
    Returns:
        用户信息字典
    """
    try:
        # 简化版本：返回模拟用户信息
        # 实际应用中应从令牌中解析用户信息
        
        # 这里应该解析JWT令牌或查询数据库获取用户信息
        user_info = {
            'id': 1,
            'username': 'demo_user',
            'is_admin': False,
            'token': token
        }
        
        return user_info
        
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        return {}

def get_current_user():
    """
    获取当前用户信息
    
    Returns:
        当前用户信息或None
    """
    return getattr(request, 'current_user', None)

def is_authenticated():
    """
    检查当前请求是否已认证
    
    Returns:
        是否已认证
    """
    return hasattr(request, 'current_user') and request.current_user is not None

def is_admin():
    """
    检查当前用户是否为管理员
    
    Returns:
        是否为管理员
    """
    user = get_current_user()
    return user and user.get('is_admin', False)



