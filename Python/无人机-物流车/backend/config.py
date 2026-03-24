"""
配置文件
包含数据库配置、API配置等
"""
import os

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # 数据库配置
    DATABASE_CONFIG = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', 'password'),
        'db': os.environ.get('DB_NAME', 'vehicle_drone_system'),
        'port': int(os.environ.get('DB_PORT', 3306))
    }
    
    # API配置
    API_PREFIX = '/api/v1'
    
    # 地图服务配置
    MAP_SERVICE_API_KEY = os.environ.get('MAP_SERVICE_API_KEY', '')
    
    # 优化算法配置
    GENETIC_ALGORITHM_CONFIG = {
        'population_size': 100,
        'generations': 1000,
        'mutation_rate': 0.1,
        'crossover_rate': 0.8,
        'elite_size': 10
    }
    
    # 数据库初始化配置
    DATABASE_INIT_CONFIG = {
        'auto_init': os.environ.get('DB_AUTO_INIT', 'True').lower() == 'true',
        'max_retries': int(os.environ.get('DB_MAX_RETRIES', 3)),
        'retry_delay': int(os.environ.get('DB_RETRY_DELAY', 5)),
        'connection_timeout': int(os.environ.get('DB_CONNECTION_TIMEOUT', 30)),
        'wait_timeout': int(os.environ.get('DB_WAIT_TIMEOUT', 60))
    }
    
    # 迁移配置
    MIGRATION_CONFIG = {
        'auto_migrate': os.environ.get('DB_AUTO_MIGRATE', 'True').lower() == 'true',
        'backup_before_migrate': os.environ.get('DB_BACKUP_BEFORE_MIGRATE', 'False').lower() == 'true',
        'migration_history_table': 'migration_history'
    }

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DATABASE_CONFIG = {
        'host': 'localhost',
        'user': 'test_user',
        'password': 'test_password',
        'db': 'test_vehicle_drone_system',
        'port': 3306
    }

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


