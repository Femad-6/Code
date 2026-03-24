/**
 * 认证工具类
 * 提供用户认证相关的工具函数
 */

// 存储键名常量
const STORAGE_KEYS = {
    AUTH_TOKEN: 'authToken',
    USER_INFO: 'userInfo',
    REFRESH_TOKEN: 'refreshToken',
    LOGIN_TIME: 'loginTime',
    TOKEN_EXPIRY: 'tokenExpiry'
};

// Token过期时间（24小时）
const TOKEN_EXPIRY_TIME = 24 * 60 * 60 * 1000;

class AuthUtils {
    constructor() {
        this.apiBaseURL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';
    }

    /**
     * 保存认证令牌
     * @param {string} token - 认证令牌
     * @param {string} refreshToken - 刷新令牌（可选）
     */
    saveToken(token, refreshToken = null) {
        try {
            localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token);
            localStorage.setItem(STORAGE_KEYS.LOGIN_TIME, Date.now().toString());
            localStorage.setItem(STORAGE_KEYS.TOKEN_EXPIRY, (Date.now() + TOKEN_EXPIRY_TIME).toString());

            if (refreshToken) {
                localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refreshToken);
            }

            console.log('认证令牌已保存');
        } catch (error) {
            console.error('保存认证令牌失败:', error);
        }
    }

    /**
     * 获取认证令牌
     * @returns {string|null} 认证令牌
     */
    getToken() {
        try {
            const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
            const expiry = localStorage.getItem(STORAGE_KEYS.TOKEN_EXPIRY);

            // 检查令牌是否过期
            if (token && expiry && Date.now() < parseInt(expiry)) {
                return token;
            } else if (token) {
                // 令牌过期，清除
                this.removeToken();
                return null;
            }

            return null;
        } catch (error) {
            console.error('获取认证令牌失败:', error);
            return null;
        }
    }

    /**
     * 移除认证令牌
     */
    removeToken() {
        try {
            localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
            localStorage.removeItem(STORAGE_KEYS.USER_INFO);
            localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
            localStorage.removeItem(STORAGE_KEYS.LOGIN_TIME);
            localStorage.removeItem(STORAGE_KEYS.TOKEN_EXPIRY);

            console.log('认证令牌已移除');
        } catch (error) {
            console.error('移除认证令牌失败:', error);
        }
    }

    /**
     * 保存用户信息
     * @param {Object} userInfo - 用户信息
     */
    saveUserInfo(userInfo) {
        try {
            localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(userInfo));
            console.log('用户信息已保存');
        } catch (error) {
            console.error('保存用户信息失败:', error);
        }
    }

    /**
     * 获取用户信息
     * @returns {Object|null} 用户信息
     */
    getUserInfo() {
        try {
            const userInfo = localStorage.getItem(STORAGE_KEYS.USER_INFO);
            return userInfo ? JSON.parse(userInfo) : null;
        } catch (error) {
            console.error('获取用户信息失败:', error);
            return null;
        }
    }

    /**
     * 检查用户是否已登录
     * @returns {boolean} 是否已登录
     */
    isLoggedIn() {
        const token = this.getToken();
        const userInfo = this.getUserInfo();
        return !!(token && userInfo);
    }

    /**
     * 检查令牌是否即将过期（1小时内）
     * @returns {boolean} 是否即将过期
     */
    isTokenExpiringSoon() {
        try {
            const expiry = localStorage.getItem(STORAGE_KEYS.TOKEN_EXPIRY);
            if (!expiry) return false;

            const expiryTime = parseInt(expiry);
            const oneHour = 60 * 60 * 1000;

            return Date.now() + oneHour > expiryTime;
        } catch (error) {
            console.error('检查令牌过期时间失败:', error);
            return false;
        }
    }

    /**
     * 获取登录时间
     * @returns {Date|null} 登录时间
     */
    getLoginTime() {
        try {
            const loginTime = localStorage.getItem(STORAGE_KEYS.LOGIN_TIME);
            return loginTime ? new Date(parseInt(loginTime)) : null;
        } catch (error) {
            console.error('获取登录时间失败:', error);
            return null;
        }
    }

    /**
     * 获取会话持续时间（毫秒）
     * @returns {number} 会话持续时间
     */
    getSessionDuration() {
        const loginTime = this.getLoginTime();
        return loginTime ? Date.now() - loginTime.getTime() : 0;
    }

    /**
     * 格式化会话持续时间
     * @returns {string} 格式化的会话时间
     */
    getFormattedSessionDuration() {
        const duration = this.getSessionDuration();
        const hours = Math.floor(duration / (1000 * 60 * 60));
        const minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));

        if (hours > 0) {
            return `${hours}小时${minutes}分钟`;
        } else {
            return `${minutes}分钟`;
        }
    }

    /**
     * 检查用户权限
     * @param {string} permission - 权限名称
     * @returns {boolean} 是否有权限
     */
    hasPermission(permission) {
        try {
            const userInfo = this.getUserInfo();
            if (!userInfo || !userInfo.permissions) {
                return false;
            }

            return userInfo.permissions.includes(permission);
        } catch (error) {
            console.error('检查用户权限失败:', error);
            return false;
        }
    }

    /**
     * 检查用户角色
     * @param {string} role - 角色名称
     * @returns {boolean} 是否有角色
     */
    hasRole(role) {
        try {
            const userInfo = this.getUserInfo();
            if (!userInfo || !userInfo.roles) {
                return false;
            }

            return userInfo.roles.includes(role);
        } catch (error) {
            console.error('检查用户角色失败:', error);
            return false;
        }
    }

    /**
     * 检查是否为管理员
     * @returns {boolean} 是否为管理员
     */
    isAdmin() {
        return this.hasRole('admin') || this.hasRole('administrator');
    }

    /**
     * 登出用户
     */
    logout() {
        this.removeToken();
        console.log('用户已登出');
    }

    /**
     * 获取认证头
     * @returns {Object} 认证头对象
     */
    getAuthHeader() {
        const token = this.getToken();
        return token ? { Authorization: `Bearer ${token}` } : {};
    }

    /**
     * 验证令牌格式
     * @param {string} token - 令牌
     * @returns {boolean} 是否有效
     */
    validateTokenFormat(token) {
        if (!token || typeof token !== 'string') {
            return false;
        }

        // 简单的令牌格式验证
        return token.length > 10;
    }

    /**
     * 刷新令牌
     * @returns {Promise<boolean>} 是否刷新成功
     */
    async refreshToken() {
        try {
            const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
            if (!refreshToken) {
                return false;
            }

            // 这里应该调用后端API刷新令牌
            // const response = await fetch(`${this.apiBaseURL}/auth/refresh`, {
            //   method: 'POST',
            //   headers: { 'Content-Type': 'application/json' },
            //   body: JSON.stringify({ refreshToken })
            // });

            // if (response.ok) {
            //   const data = await response.json();
            //   this.saveToken(data.token, data.refreshToken);
            //   return true;
            // }

            return false;
        } catch (error) {
            console.error('刷新令牌失败:', error);
            return false;
        }
    }
}

// 创建单例实例
const auth_utils = new AuthUtils();

export { auth_utils };
export default auth_utils;



