import random
n=[random.randint(1,2000) for x in range(100) ]

# 求解n的平均值
# 模型1平均值法
average = sum(n) / len(n)
x1=2*average-1
# 模型2中位数法
n.sort()
if len(n) % 2 == 0:
    median = (n[len(n) // 2 - 1] + n[len(n) // 2]) / 2
else:
    median = n[len(n) // 2]
x2=2*median-1
# 模型3两端间隔对称
x3=n[0]+n[-1]-1
# 平均间隔模型
x4=(1+1/len(n))*n[-1]-1
# 区间均分模型
x5=(1+1/(2*len(n)-1))*(n[-1]-1/2*len(n))

print(f"x1={x1},x2={x2},x3={x3},x4={x4},x5={x5}")
