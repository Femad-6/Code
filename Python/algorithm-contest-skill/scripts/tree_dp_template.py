"""
Tree DP Template for Distance-2 Independent Set Problem

Problem: Given a tree with n nodes, count the number of ways to select a subset of nodes
such that any two selected nodes have distance > 2.

State Design:
- dp[u][0]: u is not selected, parent is not selected
- dp[u][1]: u is not selected, parent is selected
- dp[u][2]: u is selected

Key Constraint: If u is not selected, at most one child can be selected
(because siblings have distance 2 through u)
"""

import sys
sys.setrecursionlimit(300000)
MOD = 998244353

def solve():
    n = int(input())
    if n == 0:
        print(0)
        return

    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)

    # DP table
    dp = [[0, 0, 0] for _ in range(n + 1)]

    def dfs(u, fa):
        """
        DFS to compute DP values for subtree rooted at u
        u: current node
        fa: parent node (0 if u is root)
        """
        # Collect children
        children = []
        for v in adj[u]:
            if v != fa:
                dfs(v, u)
                children.append(v)

        # dp[u][1]: u not selected, parent selected
        # Children cannot be selected (distance from grandparent = 2)
        dp[u][1] = 1
        for v in children:
            dp[u][1] = dp[u][1] * dp[v][0] % MOD

        # dp[u][2]: u selected
        # Children cannot be selected (distance = 1)
        dp[u][2] = 1
        for v in children:
            dp[u][2] = dp[u][2] * dp[v][1] % MOD

        # dp[u][0]: u not selected, parent not selected
        # At most one child can be selected
        # Case 1: No child is selected
        all_not_selected = 1
        for v in children:
            all_not_selected = all_not_selected * dp[v][0] % MOD

        # Case 2: Exactly one child is selected
        one_selected = 0
        k = len(children)
        for i in range(k):
            vi = children[i]
            # vi is selected, all other children are not selected
            prod = dp[vi][2]
            for j in range(k):
                if j != i:
                    vj = children[j]
                    prod = prod * dp[vj][0] % MOD
            one_selected = (one_selected + prod) % MOD

        dp[u][0] = (all_not_selected + one_selected) % MOD

    # Run DFS from root (node 1)
    dfs(1, 0)

    # Answer: root not selected (dp[1][0]) or root selected (dp[1][2])
    # Subtract 1 to exclude empty set (problem requires non-empty selection)
    ans = (dp[1][0] + dp[1][2] - 1) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
