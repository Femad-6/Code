"""
数据库初始化测试
测试数据库初始化、迁移等功能
"""
import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.services.database_init_service import DatabaseInitService
from backend.services.migration_service import MigrationService
from backend.data_access.database_connector import DatabaseConnector

class TestDatabaseInitService(unittest.TestCase):
    """数据库初始化服务测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_config = {
            'host': 'localhost',
            'user': 'test_user',
            'password': 'test_password',
            'db': 'test_db',
            'port': 3306
        }
        
        # 模拟数据库连接器
        self.mock_connector = Mock(spec=DatabaseConnector)
        
    def test_init_service_creation(self):
        """测试初始化服务创建"""
        with patch('backend.services.database_init_service.DatabaseConnector') as mock_db_class:
            mock_db_class.return_value = self.mock_connector
            
            service = DatabaseInitService(self.test_config)
            
            self.assertIsNotNone(service)
            self.assertEqual(service.db_config, self.test_config)
            self.assertIsNotNone(service.table_definitions)
            self.assertIsNotNone(service.default_data)
            self.assertIsNotNone(service.index_definitions)
    
    def test_table_definitions_structure(self):
        """测试表结构定义"""
        with patch('backend.services.database_init_service.DatabaseConnector') as mock_db_class:
            mock_db_class.return_value = self.mock_connector
            
            service = DatabaseInitService(self.test_config)
            
            # 检查必要的表是否存在
            required_tables = [
                'users', 'warehouses', 'delivery_points', 'vehicles', 
                'drones', 'tasks', 'routes', 'route_delivery_points', 
                'deliveries', 'system_config', 'migration_history'
            ]
            
            for table in required_tables:
                self.assertIn(table, service.table_definitions)
                self.assertIn('CREATE TABLE', service.table_definitions[table])
    
    def test_default_data_structure(self):
        """测试默认数据结构"""
        with patch('backend.services.database_init_service.DatabaseConnector') as mock_db_class:
            mock_db_class.return_value = self.mock_connector
            
            service = DatabaseInitService(self.test_config)
            
            # 检查默认数据表
            expected_tables = ['users', 'warehouses', 'delivery_points', 'vehicles', 'drones', 'system_config']
            
            for table in expected_tables:
                self.assertIn(table, service.default_data)
                self.assertIsInstance(service.default_data[table], list)
                if service.default_data[table]:  # 如果列表不为空
                    self.assertIsInstance(service.default_data[table][0], dict)
    
    def test_index_definitions(self):
        """测试索引定义"""
        with patch('backend.services.database_init_service.DatabaseConnector') as mock_db_class:
            mock_db_class.return_value = self.mock_connector
            
            service = DatabaseInitService(self.test_config)
            
            # 检查索引定义
            self.assertIsInstance(service.index_definitions, list)
            self.assertGreater(len(service.index_definitions), 0)
            
            for index_sql in service.index_definitions:
                self.assertIn('CREATE INDEX', index_sql)
    
    @patch('mysql.connector.connect')
    def test_check_database_exists(self, mock_connect):
        """测试检查数据库是否存在"""
        # 模拟连接和游标
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        # 模拟数据库存在
        mock_cursor.fetchone.return_value = {'Database': 'test_db'}
        
        service = DatabaseInitService(self.test_config)
        result = service.check_database_exists()
        
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch('mysql.connector.connect')
    def test_create_database(self, mock_connect):
        """测试创建数据库"""
        # 模拟连接和游标
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        service = DatabaseInitService(self.test_config)
        result = service.create_database()
        
        self.assertTrue(result)
        # 检查是否调用了创建数据库的SQL
        mock_cursor.execute.assert_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    def test_create_tables(self):
        """测试创建表"""
        with patch('backend.services.database_init_service.DatabaseConnector') as mock_db_class:
            mock_db_class.return_value = self.mock_connector
            
            service = DatabaseInitService(self.test_config)
            result = service.create_tables()
            
            self.assertTrue(result)
            # 检查是否调用了execute_query方法
            self.mock_connector.execute_query.assert_called()
    
    def test_insert_default_data(self):
        """测试插入默认数据"""
        with patch('backend.services.database_init_service.DatabaseConnector') as mock_db_class:
            mock_db_class.return_value = self.mock_connector
            
            service = DatabaseInitService(self.test_config)
            result = service.insert_default_data()
            
            self.assertTrue(result)
            # 检查是否调用了execute_many方法
            self.mock_connector.execute_many.assert_called()
    
    def test_create_indexes(self):
        """测试创建索引"""
        with patch('backend.services.database_init_service.DatabaseConnector') as mock_db_class:
            mock_db_class.return_value = self.mock_connector
            
            service = DatabaseInitService(self.test_config)
            result = service.create_indexes()
            
            self.assertTrue(result)
            # 检查是否调用了execute_query方法
            self.mock_connector.execute_query.assert_called()
    
    def test_check_initialization_status(self):
        """测试检查初始化状态"""
        with patch('backend.services.database_init_service.DatabaseConnector') as mock_db_class:
            mock_db_class.return_value = self.mock_connector
            
            # 模拟数据库存在和表存在
            service = DatabaseInitService(self.test_config)
            service.check_database_exists = Mock(return_value=True)
            self.mock_connector.fetch_one.return_value = {'Table': 'users'}
            self.mock_connector.fetch_value.return_value = 2  # 有2个用户
            
            result = service.check_initialization_status()
            
            self.assertTrue(result)
    
    def test_initialize_database_success(self):
        """测试完整初始化流程成功"""
        with patch('backend.services.database_init_service.DatabaseConnector') as mock_db_class:
            mock_db_class.return_value = self.mock_connector
            
            service = DatabaseInitService(self.test_config)
            
            # 模拟所有方法都成功
            service.check_database_exists = Mock(return_value=False)
            service.create_database = Mock(return_value=True)
            service.create_tables = Mock(return_value=True)
            service.insert_default_data = Mock(return_value=True)
            service.create_indexes = Mock(return_value=True)
            service._record_migration = Mock()
            
            result = service.initialize_database()
            
            self.assertTrue(result)
            service.create_database.assert_called_once()
            service.create_tables.assert_called_once()
            service.insert_default_data.assert_called_once()
            service.create_indexes.assert_called_once()


class TestMigrationService(unittest.TestCase):
    """数据库迁移服务测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_config = {
            'host': 'localhost',
            'user': 'test_user',
            'password': 'test_password',
            'db': 'test_db',
            'port': 3306
        }
    
    def test_migration_service_creation(self):
        """测试迁移服务创建"""
        with patch('backend.services.migration_service.DatabaseInitService') as mock_init_service:
            service = MigrationService(self.test_config)
            
            self.assertIsNotNone(service)
            self.assertEqual(service.db_config, self.test_config)
            self.assertIsNotNone(service.migrations)
    
    def test_migrations_structure(self):
        """测试迁移结构"""
        with patch('backend.services.migration_service.DatabaseInitService') as mock_init_service:
            service = MigrationService(self.test_config)
            
            # 检查迁移定义
            self.assertIn('1.0.0', service.migrations)
            migration = service.migrations['1.0.0']
            
            self.assertIn('description', migration)
            self.assertIn('up', migration)
            self.assertIn('down', migration)
            self.assertIn('dependencies', migration)
    
    def test_get_current_version(self):
        """测试获取当前版本"""
        with patch('backend.services.migration_service.DatabaseInitService') as mock_init_service:
            mock_init_service.return_value.check_database_exists.return_value = True
            mock_init_service.return_value.get_migration_history.return_value = [
                {'version': '1.0.0', 'description': 'test', 'executed_at': '2024-01-01'}
            ]
            
            service = MigrationService(self.test_config)
            version = service.get_current_version()
            
            self.assertEqual(version, '1.0.0')
    
    def test_get_latest_version(self):
        """测试获取最新版本"""
        with patch('backend.services.migration_service.DatabaseInitService') as mock_init_service:
            service = MigrationService(self.test_config)
            latest_version = service.get_latest_version()
            
            self.assertEqual(latest_version, '1.0.0')
    
    def test_get_pending_migrations(self):
        """测试获取待执行迁移"""
        with patch('backend.services.migration_service.DatabaseInitService') as mock_init_service:
            service = MigrationService(self.test_config)
            
            # 测试从None版本开始
            pending = service.get_pending_migrations(None)
            self.assertEqual(pending, ['1.0.0'])
            
            # 测试从当前版本开始
            pending = service.get_pending_migrations('1.0.0')
            self.assertEqual(pending, [])
    
    def test_check_dependencies(self):
        """测试检查依赖关系"""
        with patch('backend.services.migration_service.DatabaseInitService') as mock_init_service:
            service = MigrationService(self.test_config)
            
            # 测试无依赖的版本
            result = service.check_dependencies('1.0.0')
            self.assertTrue(result)
    
    def test_migrate_to_latest(self):
        """测试迁移到最新版本"""
        with patch('backend.services.migration_service.DatabaseInitService') as mock_init_service:
            service = MigrationService(self.test_config)
            
            # 模拟当前版本为None（未初始化）
            service.get_current_version = Mock(return_value=None)
            service.get_pending_migrations = Mock(return_value=['1.0.0'])
            service._execute_migration = Mock(return_value=True)
            
            result = service.migrate_to_latest()
            
            self.assertTrue(result)
            service._execute_migration.assert_called_once_with('1.0.0', 'up')
    
    def test_get_migration_status(self):
        """测试获取迁移状态"""
        with patch('backend.services.migration_service.DatabaseInitService') as mock_init_service:
            service = MigrationService(self.test_config)
            
            service.get_current_version = Mock(return_value='1.0.0')
            service.get_latest_version = Mock(return_value='1.0.0')
            service.get_pending_migrations = Mock(return_value=[])
            mock_init_service.return_value.get_migration_history.return_value = [
                {'version': '1.0.0'}
            ]
            
            status = service.get_migration_status()
            
            self.assertEqual(status['current_version'], '1.0.0')
            self.assertEqual(status['latest_version'], '1.0.0')
            self.assertTrue(status['is_up_to_date'])
            self.assertEqual(status['executed_migrations'], 1)


class TestDatabaseConnector(unittest.TestCase):
    """数据库连接器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_config = {
            'host': 'localhost',
            'user': 'test_user',
            'password': 'test_password',
            'db': 'test_db',
            'port': 3306
        }
    
    @patch('mysql.connector.connect')
    def test_connector_creation(self, mock_connect):
        """测试连接器创建"""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection
        
        connector = DatabaseConnector(self.test_config, auto_connect=False)
        
        self.assertIsNotNone(connector)
        self.assertEqual(connector.config, self.test_config)
    
    @patch('mysql.connector.connect')
    def test_connect_with_retry(self, mock_connect):
        """测试连接重试机制"""
        # 第一次连接失败，第二次成功
        mock_connect.side_effect = [
            Exception("Connection failed"),
            Mock()
        ]
        
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        # 第二次调用返回成功的连接
        mock_connect.side_effect = [Exception("Connection failed"), mock_connection]
        
        connector = DatabaseConnector(self.test_config, auto_connect=False)
        
        with patch('time.sleep'):  # 跳过等待时间
            result = connector.connect()
        
        # 应该重试了
        self.assertEqual(mock_connect.call_count, 2)
    
    @patch('mysql.connector.connect')
    def test_check_database_health(self, mock_connect):
        """测试数据库健康检查"""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection
        
        # 模拟健康检查查询成功
        mock_cursor.fetchone.return_value = {'health_check': 1}
        
        connector = DatabaseConnector(self.test_config, auto_connect=False)
        connector.connection = mock_connection
        connector.cursor = mock_cursor
        
        health = connector.check_database_health()
        
        self.assertEqual(health['status'], 'healthy')
        self.assertTrue(health['connected'])
    
    @patch('mysql.connector.connect')
    def test_get_database_info(self, mock_connect):
        """测试获取数据库信息"""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection
        
        # 模拟查询结果
        mock_cursor.fetchone.side_effect = [
            {'version': '8.0.25'},  # 版本查询
            {'size_mb': 10.5},      # 大小查询
            {'table_count': 5}      # 表数量查询
        ]
        
        connector = DatabaseConnector(self.test_config, auto_connect=False)
        connector.connection = mock_connection
        connector.cursor = mock_cursor
        
        info = connector.get_database_info()
        
        self.assertEqual(info['version'], '8.0.25')
        self.assertEqual(info['size_mb'], 10.5)
        self.assertEqual(info['table_count'], 5)
        self.assertTrue(info['connected'])


if __name__ == '__main__':
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_suite.addTest(unittest.makeSuite(TestDatabaseInitService))
    test_suite.addTest(unittest.makeSuite(TestMigrationService))
    test_suite.addTest(unittest.makeSuite(TestDatabaseConnector))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出测试结果
    print(f"\n测试结果:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")

