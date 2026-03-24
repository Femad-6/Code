#!/usr/bin/env python3
"""
数据库初始化验证脚本
用于验证数据库初始化功能是否正常工作
"""
import sys
import os
import time
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.config import config
from backend.services.migration_service import MigrationService
from backend.data_access.database_connector import DatabaseConnector
from backend.utils.logger import get_logger

logger = get_logger('DatabaseInitVerification')

def verify_database_connection():
    """验证数据库连接"""
    print("=" * 50)
    print("1. 验证数据库连接")
    print("=" * 50)
    
    try:
        db_config = config['development'].DATABASE_CONFIG
        connector = DatabaseConnector(db_config, auto_connect=False)
        
        # 等待数据库可用
        print("等待数据库可用...")
        if not connector.wait_for_database(timeout=30):
            print("❌ 数据库连接超时")
            return False
        
        # 测试连接
        connector.connect()
        
        # 检查健康状态
        health = connector.check_database_health()
        print(f"数据库健康状态: {health['status']}")
        
        if health['status'] == 'healthy':
            print("✅ 数据库连接正常")
            
            # 获取数据库信息
            info = connector.get_database_info()
            print(f"数据库信息: {info}")
            
            connector.close()
            return True
        else:
            print(f"❌ 数据库健康检查失败: {health['message']}")
            connector.close()
            return False
            
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def verify_database_initialization():
    """验证数据库初始化"""
    print("\n" + "=" * 50)
    print("2. 验证数据库初始化")
    print("=" * 50)
    
    try:
        db_config = config['development'].DATABASE_CONFIG
        migration_service = MigrationService(db_config)
        
        # 检查当前状态
        status = migration_service.get_migration_status()
        print(f"当前迁移状态: {status}")
        
        # 检查是否需要初始化
        if not status['is_up_to_date']:
            print("数据库需要初始化，开始执行...")
            
            # 执行迁移
            success = migration_service.migrate_to_latest()
            if success:
                print("✅ 数据库初始化成功")
            else:
                print("❌ 数据库初始化失败")
                return False
        else:
            print("✅ 数据库已是最新版本")
        
        # 再次检查状态
        final_status = migration_service.get_migration_status()
        print(f"最终迁移状态: {final_status}")
        
        migration_service.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库初始化验证失败: {e}")
        return False

def verify_tables_and_data():
    """验证表结构和数据"""
    print("\n" + "=" * 50)
    print("3. 验证表结构和数据")
    print("=" * 50)
    
    try:
        db_config = config['development'].DATABASE_CONFIG
        connector = DatabaseConnector(db_config)
        
        # 检查必要的表是否存在
        required_tables = [
            'users', 'warehouses', 'delivery_points', 'vehicles', 
            'drones', 'tasks', 'routes', 'route_delivery_points', 
            'deliveries', 'system_config', 'migration_history'
        ]
        
        print("检查表结构...")
        for table in required_tables:
            query = f"SHOW TABLES LIKE '{table}'"
            result = connector.fetch_one(query)
            if result:
                print(f"✅ 表 {table} 存在")
            else:
                print(f"❌ 表 {table} 不存在")
                return False
        
        # 检查默认数据
        print("\n检查默认数据...")
        
        # 检查用户数据
        user_count = connector.fetch_value("SELECT COUNT(*) FROM users")
        print(f"用户数量: {user_count}")
        if user_count > 0:
            print("✅ 用户数据存在")
        else:
            print("❌ 用户数据不存在")
            return False
        
        # 检查仓库数据
        warehouse_count = connector.fetch_value("SELECT COUNT(*) FROM warehouses")
        print(f"仓库数量: {warehouse_count}")
        if warehouse_count > 0:
            print("✅ 仓库数据存在")
        else:
            print("❌ 仓库数据不存在")
            return False
        
        # 检查无人机数据
        drone_count = connector.fetch_value("SELECT COUNT(*) FROM drones")
        print(f"无人机数量: {drone_count}")
        if drone_count > 0:
            print("✅ 无人机数据存在")
        else:
            print("❌ 无人机数据不存在")
            return False
        
        # 检查系统配置
        config_count = connector.fetch_value("SELECT COUNT(*) FROM system_config")
        print(f"系统配置数量: {config_count}")
        if config_count > 0:
            print("✅ 系统配置存在")
        else:
            print("❌ 系统配置不存在")
            return False
        
        # 检查迁移历史
        migration_count = connector.fetch_value("SELECT COUNT(*) FROM migration_history")
        print(f"迁移历史数量: {migration_count}")
        if migration_count > 0:
            print("✅ 迁移历史存在")
        else:
            print("❌ 迁移历史不存在")
            return False
        
        connector.close()
        return True
        
    except Exception as e:
        print(f"❌ 表结构和数据验证失败: {e}")
        return False

def verify_api_endpoints():
    """验证API端点"""
    print("\n" + "=" * 50)
    print("4. 验证API端点")
    print("=" * 50)
    
    try:
        import requests
        import json
        
        base_url = "http://localhost:5000"
        
        # 测试健康检查端点
        print("测试健康检查端点...")
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ 健康检查端点正常")
            else:
                print(f"❌ 健康检查端点异常: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print("⚠️  无法连接到API服务，请确保后端服务正在运行")
            return True  # 不强制要求API服务运行
        
        # 测试数据库状态端点
        print("测试数据库状态端点...")
        try:
            response = requests.get(f"{base_url}/api/v1/database/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 数据库状态端点正常: {data}")
            else:
                print(f"❌ 数据库状态端点异常: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print("⚠️  无法连接到数据库状态端点")
            return True  # 不强制要求API服务运行
        
        return True
        
    except ImportError:
        print("⚠️  requests库未安装，跳过API端点验证")
        return True
    except Exception as e:
        print(f"❌ API端点验证失败: {e}")
        return False

def main():
    """主函数"""
    print("数据库初始化验证脚本")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 执行验证步骤
    steps = [
        ("数据库连接", verify_database_connection),
        ("数据库初始化", verify_database_initialization),
        ("表结构和数据", verify_tables_and_data),
        ("API端点", verify_api_endpoints)
    ]
    
    results = []
    
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"❌ {step_name}验证过程中出现异常: {e}")
            results.append((step_name, False))
    
    # 输出总结
    print("\n" + "=" * 50)
    print("验证结果总结")
    print("=" * 50)
    
    all_passed = True
    for step_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{step_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有验证步骤都通过了！数据库初始化功能正常工作。")
        return 0
    else:
        print("⚠️  部分验证步骤失败，请检查相关配置和日志。")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

