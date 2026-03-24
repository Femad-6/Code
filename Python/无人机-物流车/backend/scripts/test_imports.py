#!/usr/bin/env python3
"""
测试导入脚本
验证所有模块是否可以正常导入
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def test_imports():
    """测试所有模块导入"""
    print("测试模块导入...")
    
    try:
        # 测试配置模块
        print("1. 测试配置模块...")
        from backend.config import config
        print("✅ 配置模块导入成功")
        
        # 测试数据库连接器
        print("2. 测试数据库连接器...")
        from backend.data_access.database_connector import DatabaseConnector
        print("✅ 数据库连接器导入成功")
        
        # 测试数据库初始化服务
        print("3. 测试数据库初始化服务...")
        from backend.services.database_init_service import DatabaseInitService
        print("✅ 数据库初始化服务导入成功")
        
        # 测试迁移服务
        print("4. 测试迁移服务...")
        from backend.services.migration_service import MigrationService
        print("✅ 迁移服务导入成功")
        
        # 测试应用模块
        print("5. 测试应用模块...")
        from backend.app import create_app
        print("✅ 应用模块导入成功")
        
        print("\n🎉 所有模块导入成功！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_service_creation():
    """测试服务创建"""
    print("\n测试服务创建...")
    
    try:
        from backend.config import config
        from backend.services.database_init_service import DatabaseInitService
        from backend.services.migration_service import MigrationService
        
        # 测试配置
        db_config = config['development'].DATABASE_CONFIG
        print(f"数据库配置: {db_config}")
        
        # 测试初始化服务创建（不连接数据库）
        print("创建数据库初始化服务...")
        init_service = DatabaseInitService(db_config)
        print("✅ 数据库初始化服务创建成功")
        
        # 测试迁移服务创建
        print("创建迁移服务...")
        migration_service = MigrationService(db_config)
        print("✅ 迁移服务创建成功")
        
        # 测试表结构定义
        print(f"表定义数量: {len(init_service.table_definitions)}")
        print(f"默认数据表数量: {len(init_service.default_data)}")
        print(f"索引定义数量: {len(init_service.index_definitions)}")
        
        # 测试迁移定义
        print(f"迁移版本数量: {len(migration_service.migrations)}")
        
        print("\n🎉 服务创建测试成功！")
        return True
        
    except Exception as e:
        print(f"❌ 服务创建测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("模块导入和服务创建测试")
    print("=" * 50)
    
    # 测试导入
    import_success = test_imports()
    
    if import_success:
        # 测试服务创建
        service_success = test_service_creation()
        
        if service_success:
            print("\n" + "=" * 50)
            print("🎉 所有测试都通过了！")
            print("数据库初始化功能已准备就绪。")
            print("=" * 50)
            return 0
        else:
            print("\n" + "=" * 50)
            print("⚠️  服务创建测试失败")
            print("=" * 50)
            return 1
    else:
        print("\n" + "=" * 50)
        print("⚠️  模块导入测试失败")
        print("=" * 50)
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

