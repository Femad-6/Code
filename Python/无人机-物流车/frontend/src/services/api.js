import axios from 'axios';
import { auth_utils } from '../utils/auth_utils';

// 创建axios实例
const apiClient = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 请求拦截器
apiClient.interceptors.request.use(
    (config) => {
        // 添加认证令牌
        const token = auth_utils.getToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // 添加请求时间戳
        config.metadata = { startTime: new Date() };

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器
apiClient.interceptors.response.use(
    (response) => {
        // 计算请求耗时
        const endTime = new Date();
        const duration = endTime - response.config.metadata.startTime;
        console.log(`API请求耗时: ${duration}ms - ${response.config.method?.toUpperCase()} ${response.config.url}`);

        return response;
    },
    (error) => {
        // 处理认证错误
        if (error.response?.status === 401) {
            auth_utils.removeToken();
            window.location.href = '/login';
        }

        // 处理网络错误
        if (!error.response) {
            console.error('网络错误:', error.message);
        }

        return Promise.reject(error);
    }
);

// 认证服务
export const authService = {
    login: (credentials) => apiClient.post('/api/auth/login', credentials),
    register: (userData) => apiClient.post('/api/auth/register', userData),
    logout: () => apiClient.post('/api/auth/logout'),
    verifyToken: () => apiClient.post('/api/auth/verify'),
};

// 路线服务
export const routeService = {
    createRoute: (routeData) => apiClient.post('/api/v1/routes', routeData),
    getRoute: (routeId) => apiClient.get(`/api/v1/routes/${routeId}`),
    updateRoute: (routeId, routeData) => apiClient.put(`/api/v1/routes/${routeId}`, routeData),
    deleteRoute: (routeId) => apiClient.delete(`/api/v1/routes/${routeId}`),
    optimizeRoute: (routeId, params) => apiClient.post(`/api/v1/routes/${routeId}/optimize`, params),
    calculateRouteCost: (routeId, params) => apiClient.post(`/api/v1/routes/${routeId}/cost`, params),
    getRouteStatistics: (routeId) => apiClient.get(`/api/v1/routes/${routeId}/statistics`),
    planRoute: (routeData) => apiClient.post('/api/v1/routes/plan', routeData),
};

// 无人机配送服务
export const droneService = {
    createDelivery: (deliveryData) => apiClient.post('/api/v1/drone_deliveries', deliveryData),
    getDelivery: (deliveryId) => apiClient.get(`/api/v1/drone_deliveries/${deliveryId}`),
    startDelivery: (deliveryId) => apiClient.post(`/api/v1/drone_deliveries/${deliveryId}/start`),
    completeDelivery: (deliveryId) => apiClient.post(`/api/v1/drone_deliveries/${deliveryId}/complete`),
    cancelDelivery: (deliveryId, reason) => apiClient.post(`/api/v1/drone_deliveries/${deliveryId}/cancel`, { reason }),
    getAvailableDrones: () => apiClient.get('/api/v1/drone_deliveries/available'),
    getDeliveryStatistics: () => apiClient.get('/api/v1/drone_deliveries/statistics'),
    getDeliveryStatus: (deliveryId) => apiClient.get(`/api/v1/drone_deliveries/${deliveryId}/status`),
};

// 距离计算服务
export const distanceService = {
    calculateDistance: (params) => apiClient.post('/api/v1/distances', params),
    calculateDistanceMatrix: (params) => apiClient.post('/api/v1/distance-matrix', params),
    calculateRouteDistance: (params) => apiClient.post('/api/v1/route-distance', params),
};

// 地理编码服务
export const geocodingService = {
    geocode: (address) => apiClient.post('/api/v1/geocoding', { address }),
    reverseGeocode: (coordinates) => apiClient.post('/api/v1/reverse-geocoding', coordinates),
    batchGeocode: (addresses) => apiClient.post('/api/v1/batch-geocoding', { addresses }),
};

// 优化配置服务
export const optimizationConfigService = {
    getOptimizationConfig: () => apiClient.get('/api/config/optimization'),
    updateOptimizationConfig: (config) => apiClient.put('/api/config/optimization', config),
};

// 场景比较服务
export const scenarioComparisonService = {
    compareScenarios: (params) => apiClient.post('/api/scenario/compare', params),
};

// 成本分析服务
export const costAnalysisService = {
    getCostAnalysis: (params) => apiClient.post('/api/cost/analysis', params),
};

// 用户管理服务
export const userManagementService = {
    getUsers: () => apiClient.get('/api/users'),
    updateUser: (userId, user) => apiClient.put(`/api/users/${userId}`, user),
};

// 通用API方法
export const api = {
    get: (url, config) => apiClient.get(url, config),
    post: (url, data, config) => apiClient.post(url, data, config),
    put: (url, data, config) => apiClient.put(url, data, config),
    delete: (url, config) => apiClient.delete(url, config),
    patch: (url, data, config) => apiClient.patch(url, data, config),
};

// 导出默认的API客户端
export default apiClient;



