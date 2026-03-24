import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, message } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import 'antd/dist/reset.css';

// 组件导入
import Login from './components/Login';
import MapView from './components/MapView';
import Dashboard from './components/Dashboard';

// 工具导入
import { auth_utils } from './utils/auth_utils';

// 配置消息提示
message.config({
    top: 100,
    duration: 3,
    maxCount: 3,
});

// 受保护的路由组件
const ProtectedRoute = ({ children }) => {
    const isLoggedIn = auth_utils.isLoggedIn();

    if (!isLoggedIn) {
        return <Navigate to="/login" replace />;
    }

    return children;
};

// 主应用组件
const App = () => {
    return (
        <ConfigProvider locale={zhCN}>
            <Router>
                <div className="App">
                    <Routes>
                        {/* 登录页面 */}
                        <Route
                            path="/login"
                            element={
                                auth_utils.isLoggedIn() ?
                                    <Navigate to="/dashboard" replace /> :
                                    <Login />
                            }
                        />

                        {/* 受保护的路由 */}
                        <Route
                            path="/dashboard"
                            element={
                                <ProtectedRoute>
                                    <Dashboard />
                                </ProtectedRoute>
                            }
                        />

                        {/* 地图页面 */}
                        <Route
                            path="/map"
                            element={
                                <ProtectedRoute>
                                    <MapView />
                                </ProtectedRoute>
                            }
                        />

                        {/* 默认重定向到仪表板 */}
                        <Route
                            path="/"
                            element={<Navigate to="/dashboard" replace />}
                        />

                        {/* 404页面 */}
                        <Route
                            path="*"
                            element={
                                <div style={{
                                    display: 'flex',
                                    justifyContent: 'center',
                                    alignItems: 'center',
                                    height: '100vh',
                                    flexDirection: 'column'
                                }}>
                                    <h1>404 - 页面未找到</h1>
                                    <p>您访问的页面不存在</p>
                                </div>
                            }
                        />
                    </Routes>
                </div>
            </Router>
        </ConfigProvider>
    );
};

export default App;



