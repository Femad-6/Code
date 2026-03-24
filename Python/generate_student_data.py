#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Student表的模拟数据并插入到数据库
"""

import sys
import os
import random
import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from 无人机-物流车.backend.config import config
from 无人机-物流车.backend.data_access.database_connector import DatabaseConnector

# 模拟数据配置
NUM_RECORDS = 20  # 生成的记录数量
START_YEAR = 1995  # 出生日期开始年份
END_YEAR = 2005    # 出生日期结束年份

# 模拟数据池
FIRST_NAMES = ["张", "李", "王", "刘", "陈", "杨", "赵", "黄", "周", "吴", "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗"]
LAST_NAMES = ["伟", "芳", "秀英", "娜", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞"]
MAJORS = ["计算机科学与技术", "软件工程", "信息安全", "电子信息工程", "通信工程", "自动化", "机械工程", "土木工程", "数学与应用数学", "物理学", "化学", "生物科学", "医学", "护理学", "经济学", "金融学", "会计学", "管理学", "市场营销", "汉语言文学"]
SEXES = ["男", "女"]

def generate_student_data(num_records):
    """
    生成Student表的模拟数据
    
    Args:
        num_records: 生成的记录数量
        
    Returns:
        模拟数据列表
    """
    student_data = []
    
    for i in range(1, num_records + 1):
        # 生成学号：2021 + 6位序号
        sno = f"2021{i:06d}"
        
        # 生成姓名
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        sname = f"{first_name}{last_name}"
        
        # 生成性别
        ssex = random.choice(SEXES)
        
        # 生成出生日期
        year = random.randint(START_YEAR, END_YEAR)
        month = random.randint(1, 12)
        # 根据月份生成天数
        if month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        elif month == 2:
            # 判断是否为闰年
            is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            day = random.randint(1, 29) if is_leap else random.randint(1, 28)
        else:
            day = random.randint(1, 31)
        sbirthday = datetime.date(year, month, day)
        
        # 生成专业
        smajor = random.choice(MAJORS)
        
        # 添加到数据列表
        student_data.append((sno, sname, ssex, sbirthday, smajor))
    
    return student_data

def insert_student_data(student_data):
    """
    将模拟数据插入到Student表
    
    Args:
        student_data: 模拟数据列表
        
    Returns:
        插入是否成功
    """
    # 获取数据库配置
    db_config = config['default'].DATABASE_CONFIG
    
    try:
        # 连接数据库
        with DatabaseConnector(db_config) as db:
            # 插入数据的SQL语句
            insert_sql = '''
            INSERT IGNORE INTO Student (Sno, Sname, Ssex, Sbirthday, Smajor)
            VALUES (%s, %s, %s, %s, %s);
            '''
            
            # 批量执行插入
            db.execute_many(insert_sql, student_data)
            print(f"成功插入 {len(student_data)} 条Student记录！")
            
            # 查询插入的数据，验证插入结果
            select_sql = "SELECT * FROM Student ORDER BY Sno LIMIT 10;
            results = db.fetch_all(select_sql)
            print("\n前10条插入的记录：")
            print("学号\t姓名\t性别\t出生日期\t所在专业")
            print("-" * 60)
            for record in results:
                print(f"{record['Sno']}\t{record['Sname']}\t{record['Ssex']}\t{record['Sbirthday']}\t{record['Smajor']}")
                
            # 查询总记录数
            count_sql = "SELECT COUNT(*) AS total FROM Student;
            total = db.fetch_value(count_sql)
            print(f"\nStudent表总记录数：{total}")
                
    except Exception as e:
        print(f"插入Student数据失败：{e}")
        return False
    
    return True

def main():
    """
    主函数
    """
    print("正在生成Student表的模拟数据...")
    student_data = generate_student_data(NUM_RECORDS)
    
    print(f"\n生成了 {len(student_data)} 条模拟数据：")
    print("学号\t姓名\t性别\t出生日期\t所在专业")
    print("-" * 60)
    for data in student_data[:5]:  # 显示前5条
        print(f"{data[0]}\t{data[1]}\t{data[2]}\t{data[3]}\t{data[4]}")
    if len(student_data) > 5:
        print("...")
    
    print("\n正在将数据插入到数据库...")
    insert_student_data(student_data)

if __name__ == "__main__":
    main()