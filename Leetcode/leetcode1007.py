import collections
from typing import List
class Solution:
    def minDominoRotations(self, tops: List[int], bottoms: List[int]) -> int:
        # 遍历两种可能的候选值（顶部第一个元素或底部第一个元素）
        for x in [tops[0], bottoms[0]]:
            # 检查当前候选值x是否存在于每个多米诺牌对中（顶部或底部至少有一个是x）
            if all(x in d for d in zip(tops, bottoms)):
                # 计算需要的最小旋转次数：总数 - 该数字在某一面出现的最大次数
                return len(tops) - max(tops.count(x), bottoms.count(x))
        # 如果没有符合条件的候选值，返回-1
        return -1
# Example usage:
solution = Solution()
tops = [2, 1, 2, 4, 2, 2]
bottoms = [5, 2, 6, 2, 3, 2]
result = solution.minDominoRotations(tops, bottoms)
print(result)  # Output: 2