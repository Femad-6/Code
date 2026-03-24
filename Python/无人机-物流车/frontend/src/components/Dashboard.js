import React, { useState, useEffect } from 'react';
import { Layout, Card, Row, Col, Statistic, Button, Space, Typography, message } from 'antd';
import {
    UserOutlined,
    LogoutOutlined,
    DashboardOutlined,
    EnvironmentOutlined,
    CarOutlined,
    RocketOutlined,
    BarChartOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { auth_utils } from '../utils/auth_utils';
import { format_utils } from '../utils/format_utils';
import { droneService, routeService } from '../services/api';
import './Dashboard.css';

const { Header, Content, Footer } = Layout;
const { Title, Text } = Typography;

const Dashboard = () => {
    const navigate = useNavigate();
    const [userInfo, setUserInfo] = useState(null);
    const [statistics, setStatistics] = useState({
        totalRoutes: 0,
        activeDeliveries: 0,
        availableDrones: 0,
        totalDistance: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadUserInfo();
        loadStatistics();
    }, []);

    const loadUserInfo = () => {
        const user = auth_utils.getUserInfo();
        setUserInfo(user);
    };

    const loadStatistics = async () => {
        try {
            setLoading(true);

            // 并行获取统计数据
            const [droneStats, deliveryStats] = await Promise.all([
                droneService.getAvailableDrones(),
                droneService.getDeliveryStatistics()
            ]);

            setStatistics({
                totalRoutes: 12, // 模拟数据
                activeDeliveries: deliveryStats.data?.in_progress_deliveries || 0,
                availableDrones: droneStats.data?.count || 0,
                totalDistance: 156.8 // 模拟数据
            });
        } catch (error) {
            console.error('加载统计数据失败:', error);
            message.error('加载统计数据失败');
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        auth_utils.logout();
        message.success('已退出登录');
        navigate('/login');
    };

    const handleNavigate = (path) => {
        navigate(path);
    };

    const StatCard = ({ title, value, icon, color, suffix, loading: cardLoading }) => (
        <Card className="stat-card" loading={cardLoading}>
            <Statistic
                title={title}
                value={value}
                prefix={icon}
                suffix={suffix}
                valueStyle={{ color }}
            />
        </Card>
    );

    const QuickActionCard = ({ title, description, icon, onClick, color }) => (
        <Card
            className="quick-action-card"
            hoverable
            onClick={onClick}
        >
            <div className="quick-action-content">
                <div className="quick-action-icon" style={{ color }}>
                    {icon}
                </div>
                <div className="quick-action-text">
                    <Title level={5} style={{ margin: 0, marginBottom: 4 }}>
                        {title}
                    </Title>
                    <Text type="secondary" style={{ fontSize: '12px' }}>
                        {description}
                    </Text>
                </div>
            </div>
        </Card>
    );

    return (
        <Layout className="dashboard-layout">
            <Header className="dashboard-header">
                <div className="header-content">
                    <div className="header-left">
                        <Title level={3} style={{ color: 'white', margin: 0 }}>
                            无人机-物流车系统
                        </Title>
                    </div>
                    <div className="header-right">
                        <Space>
                            <Text style={{ color: 'white' }}>
                                欢迎，{userInfo?.username || '用户'}
                            </Text>
                            <Button
                                type="text"
                                icon={<LogoutOutlined />}
                                onClick={handleLogout}
                                style={{ color: 'white' }}
                            >
                                退出
                            </Button>
                        </Space>
                    </div>
                </div>
            </Header>

            <Content className="dashboard-content">
                <div className="content-container">
                    {/* 欢迎区域 */}
                    <div className="welcome-section">
                        <Title level={2}>欢迎回来！</Title>
                        <Text type="secondary">
                            今天是 {format_utils.formatDate(new Date())}，您已登录 {format_utils.getFormattedSessionDuration()}
                        </Text>
                    </div>

                    {/* 统计卡片 */}
                    <Row gutter={[16, 16]} className="statistics-row">
                        <Col xs={24} sm={12} lg={6}>
                            <StatCard
                                title="总路线数"
                                value={statistics.totalRoutes}
                                icon={<EnvironmentOutlined />}
                                color="#1890ff"
                                loading={loading}
                            />
                        </Col>
                        <Col xs={24} sm={12} lg={6}>
                            <StatCard
                                title="活跃配送"
                                value={statistics.activeDeliveries}
                                icon={<CarOutlined />}
                                color="#52c41a"
                                loading={loading}
                            />
                        </Col>
                        <Col xs={24} sm={12} lg={6}>
                            <StatCard
                                title="可用无人机"
                                value={statistics.availableDrones}
                                icon={<RocketOutlined />}
                                color="#faad14"
                                loading={loading}
                            />
                        </Col>
                        <Col xs={24} sm={12} lg={6}>
                            <StatCard
                                title="总配送距离"
                                value={statistics.totalDistance}
                                icon={<BarChartOutlined />}
                                color="#722ed1"
                                suffix="km"
                                loading={loading}
                            />
                        </Col>
                    </Row>

                    {/* 快速操作 */}
                    <div className="quick-actions-section">
                        <Title level={3}>快速操作</Title>
                        <Row gutter={[16, 16]}>
                            <Col xs={24} sm={12} lg={8}>
                                <QuickActionCard
                                    title="查看地图"
                                    description="查看配送路线和无人机位置"
                                    icon={<EnvironmentOutlined />}
                                    color="#1890ff"
                                    onClick={() => handleNavigate('/map')}
                                />
                            </Col>
                            <Col xs={24} sm={12} lg={8}>
                                <QuickActionCard
                                    title="路线规划"
                                    description="创建和优化配送路线"
                                    icon={<DashboardOutlined />}
                                    color="#52c41a"
                                    onClick={() => message.info('路线规划功能开发中...')}
                                />
                            </Col>
                            <Col xs={24} sm={12} lg={8}>
                                <QuickActionCard
                                    title="无人机管理"
                                    description="管理无人机状态和任务"
                                    icon={<RocketOutlined />}
                                    color="#faad14"
                                    onClick={() => message.info('无人机管理功能开发中...')}
                                />
                            </Col>
                        </Row>
                    </div>

                    {/* 最近活动 */}
                    <div className="recent-activities-section">
                        <Title level={3}>最近活动</Title>
                        <Card>
                            <div className="activity-list">
                                <div className="activity-item">
                                    <Text strong>系统启动</Text>
                                    <Text type="secondary" style={{ float: 'right' }}>
                                        {format_utils.formatRelativeTime(new Date())}
                                    </Text>
                                </div>
                                <div className="activity-item">
                                    <Text strong>用户登录</Text>
                                    <Text type="secondary" style={{ float: 'right' }}>
                                        {format_utils.formatRelativeTime(new Date())}
                                    </Text>
                                </div>
                                <div className="activity-item">
                                    <Text strong>加载统计数据</Text>
                                    <Text type="secondary" style={{ float: 'right' }}>
                                        {format_utils.formatRelativeTime(new Date())}
                                    </Text>
                                </div>
                            </div>
                        </Card>
                    </div>
                </div>
            </Content>

            <Footer className="dashboard-footer">
                <Text type="secondary">
                    无人机-物流车系统 © 2024 版权所有
                </Text>
            </Footer>
        </Layout>
    );
};

export default Dashboard;



