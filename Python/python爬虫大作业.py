import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 读取CSV文件（请确认文件路径正确）
cols = ['时间编码', '品名', '价格类型', '地区', '单位', '价格']
df = pd.read_csv('d:/Code/Python/data.csv', names=cols, encoding='utf-8')

# 转换时间格式（假设时间编码格式为年份+周数，如202518表示2025年第18周）
def parse_time(code):
    year = int(str(code)[:4])
    week = int(str(code)[4:])
    return datetime.strptime(f'{year}-{week}-1', "%Y-%W-%w")

df['日期'] = df['时间编码'].apply(parse_time)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows系统字体
plt.rcParams['axes.unicode_minus'] = False

# 创建可视化图表
plt.figure(figsize=(12, 6))

# 选取部分常见蔬菜进行可视化
selected_vegetables = ['西红柿', '黄瓜', '大白菜', '西葫芦','青椒', '洋葱', '胡萝卜', '菠菜', '茄子', '生菜']
# 过滤数据
for veg in selected_vegetables:
    veg_data = df[df['品名'] == veg].sort_values('日期')
    plt.plot(veg_data['日期'], veg_data['价格'], label=veg, marker='o')

plt.title('全国平均批发价格趋势')
plt.xlabel('日期')
plt.ylabel('价格 (元/公斤)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()