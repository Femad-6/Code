"""
数据库迁移管理服务
负责数据库版本管理、升级、回滚等操作
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from backend.utils.logger import get_logger
from backend.services.database_init_service import DatabaseInitService

logger = get_logger('MigrationService')

class MigrationService:
    """数据库迁移管理服务类"""
    
    def __init__(self, db_config: Dict[str, Any]):
        """
        初始化迁移服务
        
        Args:
            db_config: 数据库配置字典
        """
        self.db_config = db_config
        self.init_service = DatabaseInitService(db_config)
        
        # 迁移版本定义
        self.migrations = self._get_migrations()
    
    def _get_migrations(self) -> Dict[str, Dict[str, Any]]:
        """获取迁移定义"""
        return {
            '1.0.0': {
                'description': '初始数据库结构创建',
                'up': self._migration_1_0_0_up,
                'down': self._migration_1_0_0_down,
                'dependencies': []
            },
            # 未来可以添加更多迁移版本
            # '1.1.0': {
            #     'description': '添加新功能表',
            #     'up': self._migration_1_1_0_up,
            #     'down': self._migration_1_1_0_down,
            #     'dependencies': ['1.0.0']
            # }
        }
    
    def _migration_1_0_0_up(self) -> bool:
        """迁移 1.0.0 升级操作"""
        try:
            logger.info("执行迁移 1.0.0 升级操作")
            return self.init_service.initialize_database()
        except Exception as e:
            logger.error(f"迁移 1.0.0 升级失败: {e}")
            return False
    
    def _migration_1_0_0_down(self) -> bool:
        """迁移 1.0.0 回滚操作"""
        try:
            logger.info("执行迁移 1.0.0 回滚操作")
            # 这里可以实现回滚逻辑，比如删除表等
            # 由于是初始版本，回滚操作可以删除整个数据库
            return self._drop_database()
        except Exception as e:
            logger.error(f"迁移 1.0.0 回滚失败: {e}")
            return False
    
    def _drop_database(self) -> bool:
        """删除数据库"""
        try:
            import mysql.connector
            from mysql.connector import Error
            
            # 获取不指定数据库的连接
            config_without_db = self.db_config.copy()
            config_without_db.pop('db', None)
            
            connection = mysql.connector.connect(
                host=config_without_db['host'],
                user=config_without_db['user'],
                password=config_without_db['password'],
                port=config_without_db.get('port', 3306),
                charset='utf8mb4'
            )
            
            cursor = connection.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.db_config['db']}")
            cursor.close()
            connection.close()
            
            logger.info(f"数据库 {self.db_config['db']} 删除成功")
            return True
            
        except Error as e:
            logger.error(f"删除数据库失败: {e}")
            return False
    
    def get_current_version(self) -> Optional[str]:
        """
        获取当前数据库版本
        
        Returns:
            当前版本号，如果未初始化则返回None
        """
        try:
            if not self.init_service.check_database_exists():
                return None
            
            history = self.init_service.get_migration_history()
            if not history:
                return None
            
            # 返回最新的版本
            return history[0]['version']
            
        except Exception as e:
            logger.error(f"获取当前版本失败: {e}")
            return None
    
    def get_latest_version(self) -> str:
        """
        获取最新版本号
        
        Returns:
            最新版本号
        """
        return max(self.migrations.keys())
    
    def get_pending_migrations(self, from_version: Optional[str] = None) -> List[str]:
        """
        获取待执行的迁移列表
        
        Args:
            from_version: 起始版本，如果为None则从当前版本开始
            
        Returns:
            待执行的迁移版本列表
        """
        if from_version is None:
            from_version = self.get_current_version()
        
        if from_version is None:
            # 如果数据库未初始化，返回所有迁移
            return list(self.migrations.keys())
        
        # 获取所有版本并排序
        all_versions = sorted(self.migrations.keys())
        
        # 找到起始版本的索引
        try:
            start_index = all_versions.index(from_version)
            # 返回起始版本之后的所有版本
            return all_versions[start_index + 1:]
        except ValueError:
            # 如果起始版本不存在，返回所有版本
            logger.warning(f"起始版本 {from_version} 不存在，返回所有迁移")
            return all_versions
    
    def check_dependencies(self, version: str) -> bool:
        """
        检查迁移依赖关系
        
        Args:
            version: 版本号
            
        Returns:
            依赖关系是否满足
        """
        if version not in self.migrations:
            logger.error(f"版本 {version} 不存在")
            return False
        
        migration = self.migrations[version]
        dependencies = migration.get('dependencies', [])
        
        if not dependencies:
            return True
        
        current_version = self.get_current_version()
        if current_version is None:
            # 如果数据库未初始化，只有没有依赖的迁移可以执行
            return len(dependencies) == 0
        
        # 检查所有依赖是否已执行
        for dep_version in dependencies:
            if not self._is_version_executed(dep_version):
                logger.error(f"依赖版本 {dep_version} 未执行")
                return False
        
        return True
    
    def _is_version_executed(self, version: str) -> bool:
        """
        检查版本是否已执行
        
        Args:
            version: 版本号
            
        Returns:
            是否已执行
        """
        try:
            history = self.init_service.get_migration_history()
            executed_versions = [record['version'] for record in history]
            return version in executed_versions
        except Exception as e:
            logger.error(f"检查版本执行状态失败: {e}")
            return False
    
    def migrate_to_version(self, target_version: str) -> bool:
        """
        迁移到指定版本
        
        Args:
            target_version: 目标版本号
            
        Returns:
            迁移是否成功
        """
        try:
            logger.info(f"开始迁移到版本 {target_version}")
            
            current_version = self.get_current_version()
            logger.info(f"当前版本: {current_version}")
            
            if current_version == target_version:
                logger.info("已经是目标版本，无需迁移")
                return True
            
            # 获取待执行的迁移
            pending_migrations = self.get_pending_migrations(current_version)
            
            if not pending_migrations:
                logger.info("没有待执行的迁移")
                return True
            
            # 过滤出目标版本之前的迁移
            target_migrations = [v for v in pending_migrations if v <= target_version]
            
            if not target_migrations:
                logger.info("目标版本之前没有待执行的迁移")
                return True
            
            # 按顺序执行迁移
            for version in target_migrations:
                if not self._execute_migration(version, 'up'):
                    logger.error(f"迁移到版本 {version} 失败")
                    return False
            
            logger.info(f"成功迁移到版本 {target_version}")
            return True
            
        except Exception as e:
            logger.error(f"迁移到版本 {target_version} 失败: {e}")
            return False
    
    def migrate_to_latest(self) -> bool:
        """
        迁移到最新版本
        
        Returns:
            迁移是否成功
        """
        latest_version = self.get_latest_version()
        return self.migrate_to_version(latest_version)
    
    def rollback_to_version(self, target_version: str) -> bool:
        """
        回滚到指定版本
        
        Args:
            target_version: 目标版本号
            
        Returns:
            回滚是否成功
        """
        try:
            logger.info(f"开始回滚到版本 {target_version}")
            
            current_version = self.get_current_version()
            if current_version is None:
                logger.warning("数据库未初始化，无法回滚")
                return False
            
            if current_version == target_version:
                logger.info("已经是目标版本，无需回滚")
                return True
            
            # 获取需要回滚的版本（从当前版本到目标版本之后）
            all_versions = sorted(self.migrations.keys(), reverse=True)
            
            try:
                current_index = all_versions.index(current_version)
                target_index = all_versions.index(target_version)
                
                # 回滚版本列表（从当前版本到目标版本之后）
                rollback_versions = all_versions[target_index + 1:current_index + 1]
                
            except ValueError:
                logger.error("版本号不存在")
                return False
            
            # 按顺序执行回滚
            for version in rollback_versions:
                if not self._execute_migration(version, 'down'):
                    logger.error(f"回滚版本 {version} 失败")
                    return False
            
            logger.info(f"成功回滚到版本 {target_version}")
            return True
            
        except Exception as e:
            logger.error(f"回滚到版本 {target_version} 失败: {e}")
            return False
    
    def _execute_migration(self, version: str, direction: str) -> bool:
        """
        执行迁移操作
        
        Args:
            version: 版本号
            direction: 方向 ('up' 或 'down')
            
        Returns:
            执行是否成功
        """
        try:
            if version not in self.migrations:
                logger.error(f"版本 {version} 不存在")
                return False
            
            migration = self.migrations[version]
            
            # 检查依赖关系（仅对升级操作）
            if direction == 'up' and not self.check_dependencies(version):
                logger.error(f"版本 {version} 的依赖关系不满足")
                return False
            
            # 执行迁移操作
            migration_func = migration.get(direction)
            if not migration_func:
                logger.error(f"版本 {version} 没有 {direction} 操作")
                return False
            
            logger.info(f"执行迁移 {version} {direction} 操作")
            success = migration_func()
            
            if success:
                # 记录迁移历史（仅对升级操作）
                if direction == 'up':
                    self.init_service._record_migration(
                        version, 
                        f"{migration['description']} ({direction})"
                    )
                logger.info(f"迁移 {version} {direction} 操作成功")
            else:
                logger.error(f"迁移 {version} {direction} 操作失败")
            
            return success
            
        except Exception as e:
            logger.error(f"执行迁移 {version} {direction} 失败: {e}")
            return False
    
    def get_migration_status(self) -> Dict[str, Any]:
        """
        获取迁移状态信息
        
        Returns:
            迁移状态字典
        """
        try:
            current_version = self.get_current_version()
            latest_version = self.get_latest_version()
            pending_migrations = self.get_pending_migrations(current_version)
            
            return {
                'current_version': current_version,
                'latest_version': latest_version,
                'pending_migrations': pending_migrations,
                'is_up_to_date': current_version == latest_version,
                'total_migrations': len(self.migrations),
                'executed_migrations': len(self.init_service.get_migration_history())
            }
            
        except Exception as e:
            logger.error(f"获取迁移状态失败: {e}")
            return {
                'current_version': None,
                'latest_version': None,
                'pending_migrations': [],
                'is_up_to_date': False,
                'total_migrations': 0,
                'executed_migrations': 0,
                'error': str(e)
            }
    
    def reset_database(self) -> bool:
        """
        重置数据库（删除并重新创建）
        
        Returns:
            重置是否成功
        """
        try:
            logger.info("开始重置数据库")
            
            # 删除数据库
            if not self._drop_database():
                logger.error("删除数据库失败")
                return False
            
            # 重新初始化
            if not self.init_service.initialize_database():
                logger.error("重新初始化数据库失败")
                return False
            
            logger.info("数据库重置成功")
            return True
            
        except Exception as e:
            logger.error(f"重置数据库失败: {e}")
            return False
    
    def close(self):
        """关闭服务"""
        if self.init_service:
            self.init_service.close()

