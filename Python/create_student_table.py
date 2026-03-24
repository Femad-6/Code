#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建Student表到SQL数据库
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from 无人机-物流车.backend.config import config
from 无人机-物流车.backend.data_access.database_connector import DatabaseConnector

def create_student_table():
    """
    创建Student表
    """
    # 获取数据库配置
    db_config = config['default'].DATABASE_CONFIG
    
    try:
        # 连接数据库
        with DatabaseConnector(db_config) as db:
            # 创建Student表的SQL语句
            create_table_sql = '''
            CREATE TABLE IF NOT EXISTS Student (
                Sno CHAR(10) NOT NULL,
                Sname VARCHAR(20),
                Ssex CHAR(2),
                Sbirthday Date,
                Smajor VARCHAR(40),
                PRIMARY KEY (Sno),
                UNIQUE KEY (Sname)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            '''
            
            # 执行创建表的SQL语句
            db.execute_query(create_table_sql)
            print("Student表创建成功！")
            
            # 显示数据库中的所有表，验证Student表是否已创建
            show_tables_sql = "SHOW TABLES"
            tables = db.fetch_all(show_tables_sql)
            print("数据库中的表：")
            for table in tables:
                print(f"  - {list(table.values())[0]}")
                
    except Exception as e:
        print(f"创建Student表失败：{e}")
        return False
    
    return True

if __name__ == "__main__":
    create_student_table()