mod = 998244353
n,m,k=map(int,input().split())
def qpow(a, b, mod):
    """快速幂计算 a^b % mod"""
    res = 1
    while b:
        if b & 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1
    return res

def inv(x):
    """计算 x 的模逆元"""
    return qpow(x, mod - 2, mod)

def C(n, r):
    """计算组合数 C(n,r)"""
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % mod * inv_fact[n-r] % mod

# 预处理阶乘和阶乘逆元
MAX = n + m + 1
fact = [1] * MAX
inv_fact = [1] * MAX
for i in range(1, MAX):
    fact[i] = fact[i-1] * i % mod
inv_fact[MAX-1] = inv(fact[MAX-1])
for i in range(MAX-2, -1, -1):
    inv_fact[i] = inv_fact[i+1] * (i+1) % mod

# DP
total = n + m
dp = [0] * (total + 1)
dp[n] = 1  # 初始状态

for _ in range(k):
    new_dp = [0] * (total + 1)
    for i in range(total + 1):  # 当前白球数量
        if dp[i] == 0:
            continue
        for j in range(6):  # 选 j 个白球
            if j > i or (5-j) > (total - i):
                continue
            # 计算概率
            ways = C(i, j) * C(total - i, 5 - j) % mod
            total_ways = C(total, 5)
            prob = ways * inv(total_ways) % mod
            
            # 计算新状态
            if j >= 3:
                new_i = i + (5 - j)
            else:
                new_i = i - j
            
            new_dp[new_i] = (new_dp[new_i] + dp[i] * prob) % mod
    
    dp = new_dp

# 答案：所有球同色的概率（全白或全黑）
ans = (dp[0] + dp[total]) % mod
print(ans)