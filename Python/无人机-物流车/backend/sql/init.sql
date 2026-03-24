-- 无人机-物流车系统数据库初始化脚本

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS vehicle_drone_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE vehicle_drone_system;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role ENUM('admin', 'user') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- 仓库表
CREATE TABLE IF NOT EXISTS warehouses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    capacity DECIMAL(10, 2) DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 配送点表
CREATE TABLE IF NOT EXISTS delivery_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    demand DECIMAL(10, 2) DEFAULT 0,
    priority INT DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 车辆表
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    capacity DECIMAL(10, 2) NOT NULL,
    max_speed DECIMAL(8, 2) NOT NULL,
    current_load DECIMAL(10, 2) DEFAULT 0,
    status ENUM('available', 'busy', 'maintenance') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 无人机表
CREATE TABLE IF NOT EXISTS drones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registration_number VARCHAR(20) UNIQUE NOT NULL,
    capacity DECIMAL(10, 2) NOT NULL,
    max_speed DECIMAL(8, 2) NOT NULL,
    max_range DECIMAL(8, 2) NOT NULL,
    battery_capacity DECIMAL(8, 2) NOT NULL,
    current_battery DECIMAL(8, 2) DEFAULT 0,
    current_load DECIMAL(10, 2) DEFAULT 0,
    status ENUM('available', 'busy', 'charging', 'maintenance') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 任务表
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    delivery_point_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    priority INT DEFAULT 0,
    deadline TIMESTAMP NULL,
    status ENUM('pending', 'assigned', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
    assigned_vehicle_id INT NULL,
    assigned_drone_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (delivery_point_id) REFERENCES delivery_points(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
    FOREIGN KEY (assigned_vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (assigned_drone_id) REFERENCES drones(id)
);

-- 路线表
CREATE TABLE IF NOT EXISTS routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    warehouse_id INT NOT NULL,
    total_distance DECIMAL(10, 2) DEFAULT 0,
    estimated_time DECIMAL(8, 2) DEFAULT 0,
    status ENUM('planned', 'active', 'completed', 'cancelled') DEFAULT 'planned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- 路线配送点关联表
CREATE TABLE IF NOT EXISTS route_delivery_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_id INT NOT NULL,
    delivery_point_id INT NOT NULL,
    sequence_order INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE,
    FOREIGN KEY (delivery_point_id) REFERENCES delivery_points(id),
    UNIQUE KEY unique_route_point (route_id, delivery_point_id)
);

-- 配送记录表
CREATE TABLE IF NOT EXISTS deliveries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    route_id INT NULL,
    vehicle_id INT NULL,
    drone_id INT NULL,
    start_time TIMESTAMP NULL,
    end_time TIMESTAMP NULL,
    actual_distance DECIMAL(10, 2) DEFAULT 0,
    actual_time DECIMAL(8, 2) DEFAULT 0,
    status ENUM('pending', 'in_progress', 'completed', 'failed') DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (route_id) REFERENCES routes(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (drone_id) REFERENCES drones(id)
);

-- 系统配置表
CREATE TABLE IF NOT EXISTS system_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入默认数据

-- 插入默认用户
INSERT INTO users (username, password, email, role) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K', 'admin@example.com', 'admin'),
('user', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K', 'user@example.com', 'user');

-- 插入默认仓库
INSERT INTO warehouses (name, address, latitude, longitude, capacity) VALUES 
('中央仓库', '北京市朝阳区中央仓库路1号', 39.9042, 116.4074, 10000.00),
('分拣中心', '上海市浦东新区分拣中心路2号', 31.2304, 121.4737, 8000.00);

-- 插入默认配送点
INSERT INTO delivery_points (name, address, latitude, longitude, demand, priority) VALUES 
('配送点A', '北京市海淀区中关村大街1号', 39.9836, 116.3164, 50.00, 1),
('配送点B', '北京市西城区西单北大街2号', 39.9139, 116.3781, 30.00, 2),
('配送点C', '北京市东城区王府井大街3号', 39.9097, 116.4134, 40.00, 1);

-- 插入默认车辆
INSERT INTO vehicles (license_plate, capacity, max_speed, status) VALUES 
('京A12345', 1000.00, 80.00, 'available'),
('京A12346', 1500.00, 75.00, 'available'),
('京A12347', 800.00, 85.00, 'available');

-- 插入默认无人机
INSERT INTO drones (registration_number, capacity, max_speed, max_range, battery_capacity, current_battery, status) VALUES 
('DRONE001', 10.00, 60.00, 50.00, 100.00, 100.00, 'available'),
('DRONE002', 15.00, 50.00, 40.00, 120.00, 85.00, 'available'),
('DRONE003', 8.00, 70.00, 60.00, 90.00, 90.00, 'available');

-- 插入系统配置
INSERT INTO system_config (config_key, config_value, description) VALUES 
('genetic_algorithm_population_size', '100', '遗传算法种群大小'),
('genetic_algorithm_generations', '1000', '遗传算法迭代次数'),
('genetic_algorithm_mutation_rate', '0.1', '遗传算法变异率'),
('genetic_algorithm_crossover_rate', '0.8', '遗传算法交叉率'),
('fuel_cost_per_km', '0.5', '每公里燃油成本'),
('time_cost_per_hour', '50', '每小时时间成本'),
('maintenance_cost_per_km', '0.1', '每公里维护成本');

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_delivery_points_status ON delivery_points(status);
CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_drones_status ON drones(status);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_routes_status ON routes(status);
CREATE INDEX idx_deliveries_status ON deliveries(status);
CREATE INDEX idx_deliveries_start_time ON deliveries(start_time);
CREATE INDEX idx_deliveries_end_time ON deliveries(end_time);



