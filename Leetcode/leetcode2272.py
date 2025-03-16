

from collections import defaultdict
class Solution:
    def largestVariance(self, s: str) -> int:
        pos = defaultdict(list)
        for i, ch in enumerate(s):
            pos[ch].append(i)

        ans = 0
        for c0, pos0 in pos.items():
            for c1, pos1 in pos.items():
                if c0 != c1:
                    i = j = 0
                    f, g = 0, float("-inf")
                    while i < len(pos0) or j < len(pos1):
                        if j == len(pos1) or (i < len(pos0) and pos0[i] < pos1[j]):
                            f, g = max(f, 0) + 1, g + 1
                            i += 1
                        else:
                            f, g = max(f, 0) - 1, max(f, g, 0) - 1
                            j += 1
                        ans = max(ans, g)
        
        return ans

s="aababbb"
print(Solution().largestVariance(s))
