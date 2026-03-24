# 无人机-物流车系统

一个基于Python Flask和React的智能配送系统，支持无人机和车辆配送路线规划与优化。

## 系统架构

```
无人机-物流车系统/
├── backend/                 # Python Flask 后端
│   ├── api/                # API 路由
│   ├── models/             # 数据模型
│   ├── services/           # 业务服务
│   ├── algorithms/         # 算法实现
│   ├── data_access/        # 数据访问层
│   ├── utils/              # 工具类
│   └── tests/              # 测试文件
├── frontend/               # React 前端
│   ├── src/
│   │   ├── components/     # React 组件
│   │   ├── services/       # API 服务
│   │   └── utils/          # 工具类
│   └── tests/              # 前端测试
├── docs/                   # 文档
└── docker-compose.yml      # Docker 配置
```

## 功能特性

### 核心功能

- 🚁 **无人机配送管理** - 支持无人机任务分配、状态监控
- 🚛 **车辆配送管理** - 支持车辆路线规划和配送任务管理
- 🗺️ **智能路线规划** - 基于遗传算法的路线优化
- 📍 **地理编码服务** - 地址与坐标转换
- 📊 **实时数据可视化** - 地图展示配送状态和路线
- 🔐 **用户认证系统** - 安全的用户登录和权限管理

### 技术特性

- ⚡ **高性能后端** - Python Flask + MySQL + Redis
- 🎨 **现代化前端** - React + Ant Design + Leaflet
- 🐳 **容器化部署** - Docker + Docker Compose
- 📱 **响应式设计** - 支持移动端和桌面端
- 🔄 **RESTful API** - 标准化的API接口
- 📈 **实时监控** - 配送状态实时更新

## 快速开始

### 环境要求

- Docker & Docker Compose
- Node.js 18+ (本地开发)
- Python 3.9+ (本地开发)
- MySQL 8.0+
- Redis 7+

### 使用Docker部署（推荐）

1. **克隆项目**

```bash
git clone <repository-url>
cd 无人机-物流车
```

2. **启动服务**

```bash
docker-compose up -d
```

3. **访问应用**

- 前端界面: <http://localhost:3000>
- 后端API: <http://localhost:5000>
- 数据库: localhost:3306

### 本地开发

#### 后端开发

1. **安装依赖**

```bash
cd backend
pip install -r requirements.txt
```

2. **配置数据库**

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE vehicle_drone_system;
```

3. **启动后端服务**

```bash
python app.py
```

#### 前端开发

1. **安装依赖**

```bash
cd frontend
npm install
```

2. **启动前端服务**

```bash
npm start
```

## API文档

### 认证接口

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/logout` - 用户登出

### 路线管理

- `POST /api/v1/routes` - 创建路线
- `GET /api/v1/routes/{id}` - 获取路线信息
- `PUT /api/v1/routes/{id}` - 更新路线
- `DELETE /api/v1/routes/{id}` - 删除路线
- `POST /api/v1/routes/{id}/optimize` - 优化路线

### 无人机配送

- `POST /api/v1/drone_deliveries` - 创建配送任务
- `GET /api/v1/drone_deliveries/{id}` - 获取配送信息
- `POST /api/v1/drone_deliveries/{id}/start` - 开始配送
- `POST /api/v1/drone_deliveries/{id}/complete` - 完成配送

### 距离计算

- `POST /api/v1/distances` - 计算距离
- `POST /api/v1/geocoding` - 地址转坐标
- `POST /api/v1/reverse-geocoding` - 坐标转地址

## 配置说明

### 环境变量

#### 后端配置

```bash
# 数据库配置
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=vehicle_drone_system
DB_PORT=3306

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379

# 应用配置
SECRET_KEY=your-secret-key
DEBUG=False
FLASK_ENV=production
```

#### 前端配置

```bash
# API配置
REACT_APP_API_URL=http://localhost:5000
```

## 开发指南

### 代码规范

- 后端使用Python PEP 8规范
- 前端使用ESLint + Prettier
- 提交信息使用Conventional Commits规范

### 测试

```bash
# 后端测试
cd backend
python -m pytest

# 前端测试
cd frontend
npm test
```

### 部署

```bash
# 构建生产版本
docker-compose -f docker-compose.prod.yml up -d
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- 项目链接: [https://github.com/yourusername/drone-delivery-system]

## 更新日志

### v1.0.0 (2024-01-01)

- 🎉 初始版本发布
- ✨ 基础配送管理功能
- 🗺️ 地图可视化界面
- 🔐 用户认证系统
- 🐳 Docker容器化部署



