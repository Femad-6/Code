import sys

sys.setrecursionlimit(300000)
MOD = 998244353

def solve():
    n = int(input())
    if n == 0:
        print(0)
        return

    # 建图
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)

    # 树形DP
    # dp[u][0]: u不选，且u的父节点也不选
    # dp[u][1]: u不选，但u的父节点被选（距离父节点为1，所以u不能选）
    # dp[u][2]: u被选

    dp = [[0, 0, 0] for _ in range(n + 1)]

    def dfs(u, fa):
        children = []
        for v in adj[u]:
            if v != fa:
                dfs(v, u)
                children.append(v)

        # dp[u][1]: u不选，父节点选 -> 子节点都不能选（距离祖父节点为2）
        # 子节点v不选，v的父节点(u)不选，所以v进入dp[v][0]
        dp[u][1] = 1
        for v in children:
            dp[u][1] = dp[u][1] * dp[v][0] % MOD

        # dp[u][2]: u被选 -> 子节点都不能选（距离为1）
        # 子节点v不选，v的父节点(u)被选，所以v进入dp[v][1]
        dp[u][2] = 1
        for v in children:
            dp[u][2] = dp[u][2] * dp[v][1] % MOD

        # dp[u][0]: u不选，父节点不选 -> 最多一个子节点被选
        # 原因：如果两个子节点都被选，它们距离为2（通过u），不合法
        # 情况1：所有子节点都不选
        all_not_selected = 1
        for v in children:
            all_not_selected = all_not_selected * dp[v][0] % MOD

        # 情况2：恰好一个子节点被选
        one_selected = 0
        k = len(children)
        for i in range(k):
            vi = children[i]
            # vi被选，其他子节点都不选
            prod = dp[vi][2]
            for j in range(k):
                if j != i:
                    vj = children[j]
                    prod = prod * dp[vj][0] % MOD
            one_selected = (one_selected + prod) % MOD

        dp[u][0] = (all_not_selected + one_selected) % MOD

    dfs(1, 0)

    # 根节点没有父节点
    # 根节点不选：dp[1][0]（最多一个子节点被选）
    # 根节点选：dp[1][2]
    # 减去全不选的情况（题目要求不能不选）
    ans = (dp[1][0] + dp[1][2] - 1) % MOD
    print(ans)

solve()
