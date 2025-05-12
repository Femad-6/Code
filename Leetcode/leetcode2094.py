from typing import List
class Solution:
    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        digits.sort()
        n = len(digits)
        ans = set()
        for i in range(n):
            if digits[i] == 0:
                continue
            for j in range(n):
                if i == j:
                    continue
                for k in range(n):
                    if i == k or j == k:
                        continue
                    if digits[k] % 2 == 0:
                        ans.add(digits[i] * 100 + digits[j] * 10 + digits[k])
        return sorted(ans)
# Example usage:
solution = Solution()
digits = [2,2,8,8,2]
result = solution.findEvenNumbers(digits)
print(result)  # Output: [222, 228, 282, 288, 822, 828, 882]