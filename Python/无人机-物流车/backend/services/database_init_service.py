"""
数据库初始化服务
负责数据库的创建、表结构初始化、默认数据插入等操作
"""
import mysql.connector
from mysql.connector import Error
from typing import Dict, List, Any, Optional, Tuple
from backend.utils.logger import get_logger
from backend.data_access.database_connector import DatabaseConnector

logger = get_logger('DatabaseInitService')

class DatabaseInitService:
    """数据库初始化服务类"""
    
    def __init__(self, db_config: Dict[str, Any]):
        """
        初始化数据库初始化服务
        
        Args:
            db_config: 数据库配置字典
        """
        self.db_config = db_config
        self.db_connector = None
        
        # 表结构定义
        self.table_definitions = self._get_table_definitions()
        
        # 默认数据定义
        self.default_data = self._get_default_data()
        
        # 索引定义
        self.index_definitions = self._get_index_definitions()
    
    def _get_table_definitions(self) -> Dict[str, str]:
        """获取表结构定义"""
        return {
            'users': """
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
                )
            """,
            'warehouses': """
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
                )
            """,
            'delivery_points': """
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
                )
            """,
            'vehicles': """
                CREATE TABLE IF NOT EXISTS vehicles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    license_plate VARCHAR(20) UNIQUE NOT NULL,
                    capacity DECIMAL(10, 2) NOT NULL,
                    max_speed DECIMAL(8, 2) NOT NULL,
                    current_load DECIMAL(10, 2) DEFAULT 0,
                    status ENUM('available', 'busy', 'maintenance') DEFAULT 'available',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """,
            'drones': """
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
                )
            """,
            'tasks': """
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
                )
            """,
            'routes': """
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
                )
            """,
            'route_delivery_points': """
                CREATE TABLE IF NOT EXISTS route_delivery_points (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    route_id INT NOT NULL,
                    delivery_point_id INT NOT NULL,
                    sequence_order INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE,
                    FOREIGN KEY (delivery_point_id) REFERENCES delivery_points(id),
                    UNIQUE KEY unique_route_point (route_id, delivery_point_id)
                )
            """,
            'deliveries': """
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
                )
            """,
            'system_config': """
                CREATE TABLE IF NOT EXISTS system_config (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    config_key VARCHAR(100) UNIQUE NOT NULL,
                    config_value TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """,
            'migration_history': """
                CREATE TABLE IF NOT EXISTS migration_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    version VARCHAR(50) NOT NULL,
                    description TEXT,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_version (version)
                )
            """
        }
    
    def _get_default_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """获取默认数据定义"""
        return {
            'users': [
                {
                    'username': 'admin',
                    'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K',
                    'email': 'admin@example.com',
                    'role': 'admin'
                },
                {
                    'username': 'user',
                    'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K',
                    'email': 'user@example.com',
                    'role': 'user'
                }
            ],
            'warehouses': [
                {
                    'name': '中央仓库',
                    'address': '北京市朝阳区中央仓库路1号',
                    'latitude': 39.9042,
                    'longitude': 116.4074,
                    'capacity': 10000.00
                },
                {
                    'name': '分拣中心',
                    'address': '上海市浦东新区分拣中心路2号',
                    'latitude': 31.2304,
                    'longitude': 121.4737,
                    'capacity': 8000.00
                }
            ],
            'delivery_points': [
                {
                    'name': '配送点A',
                    'address': '北京市海淀区中关村大街1号',
                    'latitude': 39.9836,
                    'longitude': 116.3164,
                    'demand': 50.00,
                    'priority': 1
                },
                {
                    'name': '配送点B',
                    'address': '北京市西城区西单北大街2号',
                    'latitude': 39.9139,
                    'longitude': 116.3781,
                    'demand': 30.00,
                    'priority': 2
                },
                {
                    'name': '配送点C',
                    'address': '北京市东城区王府井大街3号',
                    'latitude': 39.9097,
                    'longitude': 116.4134,
                    'demand': 40.00,
                    'priority': 1
                }
            ],
            'vehicles': [
                {
                    'license_plate': '京A12345',
                    'capacity': 1000.00,
                    'max_speed': 80.00,
                    'status': 'available'
                },
                {
                    'license_plate': '京A12346',
                    'capacity': 1500.00,
                    'max_speed': 75.00,
                    'status': 'available'
                },
                {
                    'license_plate': '京A12347',
                    'capacity': 800.00,
                    'max_speed': 85.00,
                    'status': 'available'
                }
            ],
            'drones': [
                {
                    'registration_number': 'DRONE001',
                    'capacity': 10.00,
                    'max_speed': 60.00,
                    'max_range': 50.00,
                    'battery_capacity': 100.00,
                    'current_battery': 100.00,
                    'status': 'available'
                },
                {
                    'registration_number': 'DRONE002',
                    'capacity': 15.00,
                    'max_speed': 50.00,
                    'max_range': 40.00,
                    'battery_capacity': 120.00,
                    'current_battery': 85.00,
                    'status': 'available'
                },
                {
                    'registration_number': 'DRONE003',
                    'capacity': 8.00,
                    'max_speed': 70.00,
                    'max_range': 60.00,
                    'battery_capacity': 90.00,
                    'current_battery': 90.00,
                    'status': 'available'
                }
            ],
            'system_config': [
                {
                    'config_key': 'genetic_algorithm_population_size',
                    'config_value': '100',
                    'description': '遗传算法种群大小'
                },
                {
                    'config_key': 'genetic_algorithm_generations',
                    'config_value': '1000',
                    'description': '遗传算法迭代次数'
                },
                {
                    'config_key': 'genetic_algorithm_mutation_rate',
                    'config_value': '0.1',
                    'description': '遗传算法变异率'
                },
                {
                    'config_key': 'genetic_algorithm_crossover_rate',
                    'config_value': '0.8',
                    'description': '遗传算法交叉率'
                },
                {
                    'config_key': 'fuel_cost_per_km',
                    'config_value': '0.5',
                    'description': '每公里燃油成本'
                },
                {
                    'config_key': 'time_cost_per_hour',
                    'config_value': '50',
                    'description': '每小时时间成本'
                },
                {
                    'config_key': 'maintenance_cost_per_km',
                    'config_value': '0.1',
                    'description': '每公里维护成本'
                }
            ]
        }
    
    def _get_index_definitions(self) -> List[str]:
        """获取索引定义"""
        return [
            "CREATE INDEX idx_users_username ON users(username)",
            "CREATE INDEX idx_delivery_points_status ON delivery_points(status)",
            "CREATE INDEX idx_vehicles_status ON vehicles(status)",
            "CREATE INDEX idx_drones_status ON drones(status)",
            "CREATE INDEX idx_tasks_status ON tasks(status)",
            "CREATE INDEX idx_routes_status ON routes(status)",
            "CREATE INDEX idx_deliveries_status ON deliveries(status)",
            "CREATE INDEX idx_deliveries_start_time ON deliveries(start_time)",
            "CREATE INDEX idx_deliveries_end_time ON deliveries(end_time)"
        ]
    
    def _get_connection_without_database(self) -> mysql.connector.MySQLConnection:
        """
        获取不指定数据库的连接，用于创建数据库
        
        Returns:
            MySQL连接对象
        """
        config_without_db = self.db_config.copy()
        config_without_db.pop('db', None)
        
        return mysql.connector.connect(
            host=config_without_db['host'],
            user=config_without_db['user'],
            password=config_without_db['password'],
            port=config_without_db.get('port', 3306),
            charset='utf8mb4'
        )
    
    def check_database_exists(self) -> bool:
        """
        检查数据库是否存在
        
        Returns:
            数据库是否存在
        """
        try:
            connection = self._get_connection_without_database()
            cursor = connection.cursor()
            
            cursor.execute("SHOW DATABASES LIKE %s", (self.db_config['db'],))
            result = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            exists = result is not None
            logger.info(f"数据库 {self.db_config['db']} 存在性检查: {exists}")
            return exists
            
        except Error as e:
            logger.error(f"检查数据库存在性时出错: {e}")
            return False
    
    def create_database(self) -> bool:
        """
        创建数据库
        
        Returns:
            创建是否成功
        """
        try:
            connection = self._get_connection_without_database()
            cursor = connection.cursor()
            
            # 创建数据库
            create_db_sql = f"""
                CREATE DATABASE IF NOT EXISTS {self.db_config['db']} 
                CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """
            cursor.execute(create_db_sql)
            
            # 选择数据库
            cursor.execute(f"USE {self.db_config['db']}")
            
            cursor.close()
            connection.close()
            
            logger.info(f"数据库 {self.db_config['db']} 创建成功")
            return True
            
        except Error as e:
            logger.error(f"创建数据库时出错: {e}")
            return False
    
    def _get_db_connector(self) -> DatabaseConnector:
        """获取数据库连接器"""
        if self.db_connector is None:
            self.db_connector = DatabaseConnector(self.db_config)
        return self.db_connector
    
    def create_tables(self) -> bool:
        """
        创建所有表结构
        
        Returns:
            创建是否成功
        """
        try:
            db_connector = self._get_db_connector()
            
            # 按依赖关系排序创建表
            table_order = [
                'users', 'warehouses', 'delivery_points', 'vehicles', 'drones',
                'tasks', 'routes', 'route_delivery_points', 'deliveries',
                'system_config', 'migration_history'
            ]
            
            for table_name in table_order:
                if table_name in self.table_definitions:
                    logger.info(f"创建表: {table_name}")
                    db_connector.execute_query(self.table_definitions[table_name])
            
            logger.info("所有表创建成功")
            return True
            
        except Error as e:
            logger.error(f"创建表时出错: {e}")
            return False
    
    def insert_default_data(self) -> bool:
        """
        插入默认数据
        
        Returns:
            插入是否成功
        """
        try:
            db_connector = self._get_db_connector()
            
            for table_name, data_list in self.default_data.items():
                if not data_list:
                    continue
                
                logger.info(f"插入 {table_name} 表默认数据: {len(data_list)} 条")
                
                # 构建插入语句
                columns = list(data_list[0].keys())
                placeholders = ', '.join(['%s'] * len(columns))
                insert_sql = f"""
                    INSERT IGNORE INTO {table_name} ({', '.join(columns)}) 
                    VALUES ({placeholders})
                """
                
                # 准备数据
                data_values = [tuple(row[col] for col in columns) for row in data_list]
                
                # 批量插入
                db_connector.execute_many(insert_sql, data_values)
            
            logger.info("默认数据插入成功")
            return True
            
        except Error as e:
            logger.error(f"插入默认数据时出错: {e}")
            return False
    
    def create_indexes(self) -> bool:
        """
        创建索引
        
        Returns:
            创建是否成功
        """
        try:
            db_connector = self._get_db_connector()
            
            for index_sql in self.index_definitions:
                try:
                    logger.info(f"创建索引: {index_sql}")
                    db_connector.execute_query(index_sql)
                except Error as e:
                    # 如果索引已存在，忽略错误
                    if "Duplicate key name" in str(e) or "already exists" in str(e):
                        logger.info(f"索引已存在，跳过: {index_sql}")
                        continue
                    else:
                        logger.error(f"创建索引失败: {index_sql}, 错误: {e}")
                        return False
            
            logger.info("所有索引创建成功")
            return True
            
        except Error as e:
            logger.error(f"创建索引时出错: {e}")
            return False
    
    def check_initialization_status(self) -> bool:
        """
        检查数据库初始化状态
        
        Returns:
            是否已初始化
        """
        try:
            if not self.check_database_exists():
                return False
            
            db_connector = self._get_db_connector()
            
            # 检查关键表是否存在
            required_tables = ['users', 'warehouses', 'delivery_points', 'vehicles', 'drones']
            
            for table_name in required_tables:
                check_sql = f"SHOW TABLES LIKE '{table_name}'"
                result = db_connector.fetch_one(check_sql)
                if not result:
                    logger.warning(f"表 {table_name} 不存在")
                    return False
            
            # 检查是否有默认数据
            user_count = db_connector.fetch_value("SELECT COUNT(*) FROM users")
            if user_count == 0:
                logger.warning("用户表为空，未初始化")
                return False
            
            logger.info("数据库初始化状态检查通过")
            return True
            
        except Error as e:
            logger.error(f"检查初始化状态时出错: {e}")
            return False
    
    def initialize_database(self) -> bool:
        """
        完整初始化数据库
        
        Returns:
            初始化是否成功
        """
        try:
            logger.info("开始数据库初始化...")
            
            # 1. 检查并创建数据库
            if not self.check_database_exists():
                logger.info("数据库不存在，开始创建...")
                if not self.create_database():
                    logger.error("创建数据库失败")
                    return False
            else:
                logger.info("数据库已存在")
            
            # 2. 创建表结构
            logger.info("创建表结构...")
            if not self.create_tables():
                logger.error("创建表结构失败")
                return False
            
            # 3. 插入默认数据
            logger.info("插入默认数据...")
            if not self.insert_default_data():
                logger.error("插入默认数据失败")
                return False
            
            # 4. 创建索引
            logger.info("创建索引...")
            if not self.create_indexes():
                logger.error("创建索引失败")
                return False
            
            # 5. 记录迁移历史
            self._record_migration('1.0.0', '初始数据库结构创建')
            
            logger.info("数据库初始化完成")
            return True
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            return False
        finally:
            if self.db_connector:
                self.db_connector.close()
    
    def _record_migration(self, version: str, description: str) -> None:
        """
        记录迁移历史
        
        Args:
            version: 版本号
            description: 描述
        """
        try:
            db_connector = self._get_db_connector()
            
            insert_sql = """
                INSERT IGNORE INTO migration_history (version, description) 
                VALUES (%s, %s)
            """
            db_connector.execute_query(insert_sql, (version, description))
            
            logger.info(f"记录迁移历史: {version} - {description}")
            
        except Error as e:
            logger.warning(f"记录迁移历史失败: {e}")
    
    def get_migration_history(self) -> List[Dict[str, Any]]:
        """
        获取迁移历史
        
        Returns:
            迁移历史列表
        """
        try:
            db_connector = self._get_db_connector()
            
            query = """
                SELECT version, description, executed_at 
                FROM migration_history 
                ORDER BY executed_at DESC
            """
            return db_connector.fetch_all(query)
            
        except Error as e:
            logger.error(f"获取迁移历史失败: {e}")
            return []
    
    def close(self):
        """关闭数据库连接"""
        if self.db_connector:
            self.db_connector.close()
            self.db_connector = None

