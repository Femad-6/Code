from typing import List
from heapq import heappop, heappush
from math import inf
class Solution:
    def minTimeToReach(self, moveTime: List[List[int]]) -> int:
        n, m = len(moveTime), len(moveTime[0])
        dis = [[inf] * m for _ in range(n)]
        dis[0][0] = 0
        h = [(0, 0, 0)]
        while True:
            d, i, j = heappop(h)
            if i == n - 1 and j == m - 1:
                return d
            if d > dis[i][j]:
                continue
            for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):  # 枚举周围四个格子
                if 0 <= x < n and 0 <= y < m:
                    new_dis = max(d, moveTime[x][y]) + 1
                    if new_dis < dis[x][y]:
                        dis[x][y] = new_dis
                        heappush(h, (new_dis, x, y))

        return -1  # 如果无法到达终点，返回-1（理论上不会到达这个情况）
# 3341. 到达终点的最小时间


# Example usage:
solution = Solution()
moveTime = [[0,4],[4,4]]
result = solution.minTimeToReach(moveTime)
print(result)  # Output: 6