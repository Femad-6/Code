"""
数据库连接器
提供数据库操作的基础功能
"""
import mysql.connector
from mysql.connector import Error
from typing import Optional, Tuple, Any, List, Dict
import json
import time
from backend.utils.logger import get_logger

logger = get_logger('DatabaseConnector')

class DatabaseConnector:
    """数据库连接器类"""
    
    def __init__(self, config: Dict[str, Any], auto_connect: bool = True):
        """
        初始化数据库连接器
        
        Args:
            config: 数据库配置字典
            auto_connect: 是否自动连接数据库
        """
        self.config = config
        self.connection = None
        self.cursor = None
        self.max_retries = 3
        self.retry_delay = 5
        
        if auto_connect:
            self.connect()
    
    def connect(self, retry_count: int = 0):
        """
        建立数据库连接
        
        Args:
            retry_count: 重试次数
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['db'],
                port=self.config.get('port', 3306),
                charset='utf8mb4',
                autocommit=True,
                connection_timeout=30
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                logger.info(f"成功连接到MySQL数据库: {self.config['db']}")
            else:
                raise Exception("无法建立数据库连接")
                
        except Error as e:
            logger.error(f"数据库连接错误: {e}")
            
            # 重试逻辑
            if retry_count < self.max_retries:
                logger.info(f"等待 {self.retry_delay} 秒后重试连接... (第 {retry_count + 1} 次)")
                time.sleep(self.retry_delay)
                return self.connect(retry_count + 1)
            else:
                logger.error(f"数据库连接失败，已重试 {self.max_retries} 次")
                raise
    
    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
        """
        执行SQL查询（INSERT, UPDATE, DELETE）
        
        Args:
            query: SQL查询语句
            params: 查询参数
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            logger.debug(f"执行查询成功: {query[:100]}...")
            
        except Error as e:
            logger.error(f"执行查询失败: {e}")
            self.connection.rollback()
            raise
    
    def fetch_all(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        """
        获取所有查询结果
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            查询结果列表
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            logger.debug(f"获取到 {len(results)} 条记录")
            return results
            
        except Error as e:
            logger.error(f"查询失败: {e}")
            raise
    
    def fetch_one(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
        """
        获取单条查询结果
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            查询结果或None
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            result = self.cursor.fetchone()
            logger.debug(f"获取到单条记录: {result is not None}")
            return result
            
        except Error as e:
            logger.error(f"查询失败: {e}")
            raise
    
    def fetch_value(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Any]:
        """
        获取单个值
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            查询结果的值或None
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            result = self.cursor.fetchone()
            if result:
                # 返回第一个字段的值
                return list(result.values())[0]
            return None
            
        except Error as e:
            logger.error(f"查询失败: {e}")
            raise
    
    def insert_and_get_id(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> int:
        """
        插入数据并返回自增ID
        
        Args:
            query: SQL插入语句
            params: 插入参数
            
        Returns:
            插入记录的自增ID
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            insert_id = self.cursor.lastrowid
            logger.debug(f"插入成功，ID: {insert_id}")
            return insert_id
            
        except Error as e:
            logger.error(f"插入失败: {e}")
            self.connection.rollback()
            raise
    
    def execute_many(self, query: str, params_list: List[Tuple[Any, ...]]) -> None:
        """
        批量执行SQL语句
        
        Args:
            query: SQL语句
            params_list: 参数列表
        """
        try:
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            logger.debug(f"批量执行成功，影响 {len(params_list)} 条记录")
            
        except Error as e:
            logger.error(f"批量执行失败: {e}")
            self.connection.rollback()
            raise
    
    def begin_transaction(self):
        """开始事务"""
        self.connection.start_transaction()
        logger.debug("开始事务")
    
    def commit_transaction(self):
        """提交事务"""
        self.connection.commit()
        logger.debug("提交事务")
    
    def rollback_transaction(self):
        """回滚事务"""
        self.connection.rollback()
        logger.debug("回滚事务")
    
    def close(self):
        """关闭数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger.info("数据库连接已关闭")
        except Error as e:
            logger.error(f"关闭数据库连接时出错: {e}")
    
    def is_connected(self) -> bool:
        """检查数据库连接状态"""
        try:
            if self.connection and self.connection.is_connected():
                return True
            return False
        except:
            return False
    
    def reconnect(self):
        """重新连接数据库"""
        self.close()
        self.connect()
        logger.info("数据库重新连接成功")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if exc_type:
            self.rollback_transaction()
        else:
            self.commit_transaction()
        self.close()
    
    def check_database_health(self) -> Dict[str, Any]:
        """
        检查数据库健康状态
        
        Returns:
            健康状态信息
        """
        try:
            if not self.is_connected():
                return {
                    'status': 'unhealthy',
                    'message': '数据库连接断开',
                    'connected': False
                }
            
            # 检查基本查询
            self.cursor.execute("SELECT 1 as health_check")
            result = self.cursor.fetchone()
            
            if result and result['health_check'] == 1:
                return {
                    'status': 'healthy',
                    'message': '数据库连接正常',
                    'connected': True,
                    'database': self.config['db'],
                    'host': self.config['host'],
                    'port': self.config.get('port', 3306)
                }
            else:
                return {
                    'status': 'unhealthy',
                    'message': '数据库查询异常',
                    'connected': True
                }
                
        except Error as e:
            logger.error(f"数据库健康检查失败: {e}")
            return {
                'status': 'unhealthy',
                'message': f'数据库健康检查失败: {str(e)}',
                'connected': False
            }
    
    def wait_for_database(self, timeout: int = 60) -> bool:
        """
        等待数据库可用
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            数据库是否可用
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if self.is_connected():
                    # 测试查询
                    self.cursor.execute("SELECT 1")
                    return True
            except:
                pass
            
            logger.info(f"等待数据库可用... (已等待 {int(time.time() - start_time)} 秒)")
            time.sleep(2)
        
        logger.error(f"等待数据库超时 ({timeout} 秒)")
        return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        获取数据库信息
        
        Returns:
            数据库信息
        """
        try:
            if not self.is_connected():
                return {'error': '数据库未连接'}
            
            # 获取数据库版本
            self.cursor.execute("SELECT VERSION() as version")
            version_result = self.cursor.fetchone()
            
            # 获取数据库大小
            self.cursor.execute(f"""
                SELECT 
                    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb
                FROM information_schema.tables 
                WHERE table_schema = '{self.config['db']}'
            """)
            size_result = self.cursor.fetchone()
            
            # 获取表数量
            self.cursor.execute(f"""
                SELECT COUNT(*) as table_count
                FROM information_schema.tables 
                WHERE table_schema = '{self.config['db']}'
            """)
            table_count_result = self.cursor.fetchone()
            
            return {
                'database': self.config['db'],
                'host': self.config['host'],
                'port': self.config.get('port', 3306),
                'version': version_result['version'] if version_result else 'Unknown',
                'size_mb': size_result['size_mb'] if size_result else 0,
                'table_count': table_count_result['table_count'] if table_count_result else 0,
                'connected': True
            }
            
        except Error as e:
            logger.error(f"获取数据库信息失败: {e}")
            return {
                'error': str(e),
                'connected': False
            }
    
    def __del__(self):
        """析构函数"""
        self.close()


