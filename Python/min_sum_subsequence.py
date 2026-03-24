from collections import deque

n, k = map(int, input().split())
a = [0] + list(map(int, input().split()))

# dp[i] = 以第i个数结尾的子序列的最小和
dp = [0] * (n + 1)
dp[1] = a[1]

q = deque([1])  # 单调队列，存下标，dp值递增

for i in range(2, n + 1):
    left = i - k
    
    # 弹出超出窗口范围的下标
    while q and q[0] < left:
        q.popleft()
    
    # 状态转移：dp[i] = min(dp[j]) + a[i]
    dp[i] = dp[q[0]] + a[i]
    
    # 维护单调递增性质
    while q and dp[q[-1]] >= dp[i]:
        q.pop()
    
    q.append(i)

print(dp[n])
