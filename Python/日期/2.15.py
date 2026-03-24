n = int(input())

# f[x] 表示数字x在杨辉三角中出现的次数
f = [0] * (n + 1)

# 初始化
# 2只出现1次（在第2行的中间，对称位置相同）
if n >= 2:
    f[2] = 1

# 对于x >= 3，至少出现2次（作为C(x,1)和C(x,x-1)）
for i in range(3, n + 1):
    f[i] = 2

# 遍历杨辉三角的第3行到第n-1行
# 计算内部的组合数（k从2开始，因为k=0和k=1已经计算过了）
for r in range(3, n):
    value = r  # C(r, 1) = r
    for k in range(2, r // 2 + 1):
        # C(r, k) = C(r, k-1) * (r-k+1) // k
        value = value * (r - k + 1) // k
        if value > n:
            break
        else:
            # 检查是否是中间位置
            if k == r // 2 and r % 2 == 0:
                f[value] += 1  # 中间位置只算一次
            else:
                f[value] += 2  # 对称位置算两次

# 统计每个f[x]值出现的次数
freq = {}
for x in range(2, n + 1):
    fx = f[x]
    freq[fx] = freq.get(fx, 0) + 1

# 按f[x]值从小到大输出
for v in sorted(freq.keys()):
    print(v, freq[v])
