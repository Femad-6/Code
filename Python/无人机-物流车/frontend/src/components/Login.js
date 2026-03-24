import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, Card, message, Typography } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import axios from 'axios';
import { auth_utils } from '../utils/auth_utils';
import './Login.css';

const { Title } = Typography;

const Login = () => {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (values) => {
        setLoading(true);
        try {
            const response = await axios.post('/api/auth/login', {
                username: values.username,
                password: values.password,
            });

            if (response.data.success) {
                const { token } = response.data;
                auth_utils.saveToken(token);
                message.success('登录成功！');
                navigate('/dashboard');
            } else {
                message.error(response.data.message || '登录失败');
            }
        } catch (error) {
            console.error('Login failed:', error);
            if (error.response?.data?.message) {
                message.error(error.response.data.message);
            } else {
                message.error('登录失败，请检查网络连接');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = () => {
        navigate('/register');
    };

    return (
        <div className="login-container">
            <Card className="login-card" bordered={false}>
                <div className="login-header">
                    <Title level={2} className="login-title">
                        无人机-物流车系统
                    </Title>
                    <p className="login-subtitle">请登录您的账户</p>
                </div>

                <Form
                    name="login"
                    onFinish={handleLogin}
                    autoComplete="off"
                    size="large"
                >
                    <Form.Item
                        name="username"
                        rules={[
                            { required: true, message: '请输入用户名!' },
                            { min: 3, message: '用户名至少3个字符!' }
                        ]}
                    >
                        <Input
                            prefix={<UserOutlined />}
                            placeholder="用户名"
                        />
                    </Form.Item>

                    <Form.Item
                        name="password"
                        rules={[
                            { required: true, message: '请输入密码!' },
                            { min: 6, message: '密码至少6个字符!' }
                        ]}
                    >
                        <Input.Password
                            prefix={<LockOutlined />}
                            placeholder="密码"
                        />
                    </Form.Item>

                    <Form.Item>
                        <Button
                            type="primary"
                            htmlType="submit"
                            loading={loading}
                            block
                            className="login-button"
                        >
                            登录
                        </Button>
                    </Form.Item>

                    <Form.Item>
                        <Button
                            type="link"
                            onClick={handleRegister}
                            block
                            className="register-button"
                        >
                            还没有账户？立即注册
                        </Button>
                    </Form.Item>
                </Form>
            </Card>
        </div>
    );
};

export default Login;



