mod = 10**9 + 7

n = int(input())
a = list(map(int, input().split()))

# 统计每个数值出现的次数
from collections import Counter
cnt = Counter(a)

ans = 0

# 情况1：x != y，选 (x,y,y,x) 和 (y,x,x,y) 两种模式
# 但由于是有序四元组，(x,y,y,x) 本身就有 A(cnt[x],2) * A(cnt[y],2) 种
# 而 (y,x,x,y) 会在遍历到 (y,x) 时计算，所以只需要遍历 x < y 或 x != y 都可以
# 实际上，对于有序四元组，(x,y,y,x) 和 (y,x,x,y) 是不同的方案

values = list(cnt)

# 遍历所有不同的数值对 (x, y)，包括 x == y 的情况
for i, x in enumerate(values):
    cx = cnt[x]
    # x == y 的情况：四个位置都选同一个值，但需要4个不同的下标
    # 方案数：A(cx, 4)
    if cx >= 4:
        ans = (ans + cx * (cx - 1) * (cx - 2) * (cx - 3)) % mod
    
    # x != y 的情况：选 (x, y, y, x)，即 a_i=x, a_j=y, a_p=y, a_q=x
    # 方案数：A(cx, 2) * A(cy, 2) = cx*(cx-1) * cy*(cy-1)
    for j in range(i + 1, len(values)):
        y = values[j]
        cy = cnt[y]
        if cx >= 2 and cy >= 2:
            ways = (cx * (cx - 1) * cy * (cy - 1)) % mod
            # 两种模式：(x,y,y,x) 和 (y,x,x,y)
            ans = (ans + 2 * ways) % mod

print(ans)
