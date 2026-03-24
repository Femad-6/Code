from pulp import *

# 定义数据
shebei = [1, 2, 3, 4, 5, 6]  # 6台设备
qiye = [1, 2, 3, 4]           # 4家企业

# 效益矩阵c (6行4列)
c = [
    [4, 2, 3, 4],
    [6, 4, 5, 5],
    [7, 6, 7, 6],
    [7, 8, 8, 6],
    [7, 9, 8, 6],
    [7, 10, 8, 6]
]

# 创建问题实例
prob = LpProblem("Equipment_Assignment", LpMaximize)

# 创建0-1决策变量
x = LpVariable.dicts("x", 
                     ((i, j) for i in shebei for j in qiye),
                     cat=LpBinary)

# 目标函数：最大化总效益
prob += lpSum(c[i-1][j-1] * x[(i, j)] for i in shebei for j in qiye)

# 约束1：每个企业至少分配2台设备
for j in qiye:
    prob += lpSum(x[(i, j)] for i in shebei) >= 2

# 约束2：每台设备只能分配给一个企业
for i in shebei:
    prob += lpSum(x[(i, j)] for j in qiye) == 1

# 求解问题
status = prob.solve()

# 输出结果
print(f"求解状态: {LpStatus[status]}")
print(f"最大总效益: {value(prob.objective)}\n")

# 打印分配方案
print("设备分配方案 (设备→企业):")
for i in shebei:
    for j in qiye:
        if value(x[(i, j)]) == 1:
            print(f"设备 {i} → 企业 {j} (效益: {c[i-1][j-1]})")