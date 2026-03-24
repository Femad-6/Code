from typing import List
from itertools import accumulate

class Solution:
    def isZeroArray(self, nums: List[int], queries: List[List[int]]) -> bool:
        diff = [0] * (len(nums) + 1)
        for l, r in queries:
            # 区间 [l,r] 中的数都加一
            diff[l] += 1
            diff[r + 1] -= 1

        for x, sum_d in zip(nums, accumulate(diff)):
            # 此时 sum_d 表示 x=nums[i] 要减掉多少
            if x > sum_d:  # x 无法变成 0
                return False
        return True



if __name__ == "__main__":
    obj = Solution()
    nums = [1, 0, 1]
    queries = [[0, 2]]
    print(obj.isZeroArray(nums, queries))