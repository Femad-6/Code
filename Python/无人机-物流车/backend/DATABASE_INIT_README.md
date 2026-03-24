# 数据库初始化功能说明

## 概述

本项目已将数据库初始化从SQL文件迁移到Python代码中，提供了更灵活、可维护的数据库管理方案。

## 主要特性

### 1. 自动初始化

- 应用启动时自动检查数据库状态
- 自动创建数据库、表结构、默认数据和索引
- 支持数据库版本管理和迁移

### 2. 迁移管理

- 支持数据库版本控制
- 提供升级和回滚功能
- 记录迁移历史

### 3. 健康检查

- 数据库连接状态监控
- 自动重连机制
- 连接超时和重试配置

## 文件结构

```
backend/
├── services/
│   ├── database_init_service.py    # 数据库初始化服务
│   └── migration_service.py        # 数据库迁移管理服务
├── data_access/
│   └── database_connector.py       # 数据库连接器（已增强）
├── config.py                       # 配置文件（已更新）
├── app.py                          # 应用主文件（已更新）
└── scripts/
    └── verify_database_init.py     # 验证脚本
```

## 配置说明

### 环境变量

```bash
# 数据库初始化配置
DB_AUTO_INIT=true                    # 是否自动初始化
DB_MAX_RETRIES=3                     # 最大重试次数
DB_RETRY_DELAY=5                     # 重试延迟（秒）
DB_CONNECTION_TIMEOUT=30             # 连接超时（秒）
DB_WAIT_TIMEOUT=60                   # 等待超时（秒）

# 迁移配置
DB_AUTO_MIGRATE=true                 # 是否自动迁移
DB_BACKUP_BEFORE_MIGRATE=false       # 迁移前是否备份
```

### 配置文件

在 `backend/config.py` 中新增了以下配置：

```python
# 数据库初始化配置
DATABASE_INIT_CONFIG = {
    'auto_init': True,
    'max_retries': 3,
    'retry_delay': 5,
    'connection_timeout': 30,
    'wait_timeout': 60
}

# 迁移配置
MIGRATION_CONFIG = {
    'auto_migrate': True,
    'backup_before_migrate': False,
    'migration_history_table': 'migration_history'
}
```

## 使用方法

### 1. 自动初始化（推荐）

应用启动时会自动执行数据库初始化：

```bash
# 启动应用
python backend/app.py

# 或使用Docker
docker-compose up backend
```

### 2. 手动初始化

```python
from backend.services.migration_service import MigrationService
from backend.config import config

# 创建迁移服务
migration_service = MigrationService(config['development'].DATABASE_CONFIG)

# 迁移到最新版本
success = migration_service.migrate_to_latest()

# 关闭服务
migration_service.close()
```

### 3. 检查数据库状态

```python
from backend.services.migration_service import MigrationService
from backend.config import config

migration_service = MigrationService(config['development'].DATABASE_CONFIG)

# 获取迁移状态
status = migration_service.get_migration_status()
print(f"当前版本: {status['current_version']}")
print(f"最新版本: {status['latest_version']}")
print(f"是否最新: {status['is_up_to_date']}")

migration_service.close()
```

### 4. 重置数据库

```python
from backend.services.migration_service import MigrationService
from backend.config import config

migration_service = MigrationService(config['development'].DATABASE_CONFIG)

# 重置数据库（删除并重新创建）
success = migration_service.reset_database()

migration_service.close()
```

## API端点

新增了以下API端点用于数据库管理：

### 1. 获取数据库状态

```http
GET /api/v1/database/status
```

响应示例：

```json
{
    "status": "success",
    "data": {
        "current_version": "1.0.0",
        "latest_version": "1.0.0",
        "pending_migrations": [],
        "is_up_to_date": true,
        "total_migrations": 1,
        "executed_migrations": 1
    }
}
```

### 2. 执行数据库迁移

```http
POST /api/v1/database/migrate
```

响应示例：

```json
{
    "status": "success",
    "message": "数据库迁移成功"
}
```

### 3. 重置数据库

```http
POST /api/v1/database/reset
```

响应示例：

```json
{
    "status": "success",
    "message": "数据库重置成功"
}
```

## 验证和测试

### 1. 运行验证脚本

```bash
# 验证数据库初始化功能
python backend/scripts/verify_database_init.py
```

### 2. 运行单元测试

```bash
# 运行数据库初始化测试
python -m pytest backend/tests/test_database_init.py -v
```

### 3. 手动测试

```bash
# 启动应用并检查日志
python backend/app.py

# 检查数据库状态API
curl http://localhost:5000/api/v1/database/status
```

## Docker部署

### 1. 更新后的docker-compose.yml

主要变化：

- 移除了SQL文件挂载
- 添加了服务依赖条件
- 增加了启动延迟

```yaml
services:
  mysql:
    # ... MySQL配置
    volumes:
      - mysql_data:/var/lib/mysql
      # 移除了SQL文件挂载
  
  backend:
    # ... 后端配置
    depends_on:
      mysql:
        condition: service_started
    command: sh -c "sleep 10 && python app.py"
```

### 2. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
```

## 故障排除

### 1. 数据库连接失败

**问题**: 应用启动时数据库连接失败

**解决方案**:

- 检查数据库服务是否启动
- 验证数据库配置是否正确
- 增加重试次数和延迟时间

```python
# 在config.py中调整配置
DATABASE_INIT_CONFIG = {
    'max_retries': 5,        # 增加重试次数
    'retry_delay': 10,       # 增加延迟时间
    'wait_timeout': 120      # 增加等待超时
}
```

### 2. 初始化失败

**问题**: 数据库初始化过程中失败

**解决方案**:

- 检查数据库权限
- 查看详细错误日志
- 手动执行初始化

```python
# 手动初始化
from backend.services.migration_service import MigrationService
migration_service = MigrationService(db_config)
migration_service.migrate_to_latest()
```

### 3. 表结构不匹配

**问题**: 现有数据库表结构与新版本不匹配

**解决方案**:

- 备份现有数据
- 重置数据库
- 重新导入数据

```python
# 重置数据库
migration_service.reset_database()
```

## 迁移指南

### 从SQL文件迁移

如果您之前使用SQL文件进行数据库初始化，请按以下步骤迁移：

1. **备份现有数据**

   ```bash
   mysqldump -u username -p database_name > backup.sql
   ```

2. **更新代码**
   - 确保所有新文件都已部署
   - 更新配置文件

3. **测试新功能**

   ```bash
   python backend/scripts/verify_database_init.py
   ```

4. **部署到生产环境**
   - 先在测试环境验证
   - 逐步部署到生产环境

## 最佳实践

### 1. 开发环境

- 使用自动初始化功能
- 定期运行验证脚本
- 保持测试数据的一致性

### 2. 生产环境

- 谨慎使用重置功能
- 定期备份数据库
- 监控数据库健康状态

### 3. 版本管理

- 为每个数据库变更创建迁移
- 测试迁移的升级和回滚
- 记录迁移历史

## 支持

如果您在使用过程中遇到问题，请：

1. 查看应用日志
2. 运行验证脚本
3. 检查配置文件
4. 参考故障排除部分

---

**注意**: 本功能已完全替代原有的SQL文件初始化方式，请确保在生产环境部署前进行充分测试。

