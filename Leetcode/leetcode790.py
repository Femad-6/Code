from typing import List
# 790. Domino and Tromino Tiling
class Solution:
    def numTilings(self, n: int) -> int:
        MOD = 10**9 + 7  # 定义模数，用于防止结果过大
        # 初始化动态规划数组，dp[i]表示填满前i列的平铺方式数
        dp = [0] * (n + 1)
        # 初始化边界条件，dp[0] = 1，dp[1] = 1，dp[2] = 2
        dp[0], dp[1], dp[2] = 1, 1, 2
        # 从第3列开始计算
        for i in range(3, n + 1):
            # 计算填满前i列的平铺方式数
            dp[i] = (dp[i - 1] + dp[i - 2] + 2 * sum(dp[:i - 2])) % MOD
        # 返回填满前n列的平铺方式数
        return dp[n]
# Example usage:
solution = Solution()
n = 3
result = solution.numTilings(n)
print(result)  # Output: 5
