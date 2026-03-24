"""
Digit DP Template for Range Counting Problems

Problem: Count numbers in range [0, n] satisfying digit-based constraints.
Example: Count numbers where sum of absolute differences between adjacent digits <= m

Key Insight: Use memoization with tight constraint to handle large ranges (up to 10^18) efficiently.

State Design:
- pos: current digit position being processed
- last: previous digit (for constraint checking)
- sum_val: accumulated value (e.g., sum of differences)
- tight: whether current prefix equals n's prefix (bounded by n)
"""

from functools import lru_cache

def solve():
    """
    Example: Count "tidy numbers" where sum of adjacent digit differences <= m
    """
    n, m = map(int, input().split())

    # Convert n to digit list for digit-by-digit processing
    digits = list(map(int, str(n)))

    @lru_cache(maxsize=None)
    def dfs(pos, last, sum_val, tight):
        """
        Count valid numbers from position pos to end

        Args:
            pos: current position in digits list
            last: previous digit (10 means no previous digit / leading zero)
            sum_val: current accumulated sum (e.g., sum of differences)
            tight: True if current prefix equals n's prefix (bounded)

        Returns:
            Number of valid configurations
        """
        # Pruning: if accumulated value exceeds limit, no valid numbers
        if sum_val > m:
            return 0

        # Base case: processed all digits
        if pos == len(digits):
            return 1

        res = 0
        # Determine upper bound for current digit
        upper = digits[pos] if tight else 9

        for d in range(upper + 1):
            # Update tight constraint
            new_tight = tight and (d == upper)

            if last == 10:  # Leading zero state (no previous digit)
                if d == 0:
                    # Continue leading zero state
                    res += dfs(pos + 1, 10, 0, new_tight)
                else:
                    # First non-zero digit, start counting
                    res += dfs(pos + 1, d, 0, new_tight)
            else:
                # Calculate new accumulated value
                new_sum = sum_val + abs(d - last)
                res += dfs(pos + 1, d, new_sum, new_tight)

        return res

    # Start from position 0, no previous digit, sum=0, tight=True
    ans = dfs(0, 10, 0, True)
    print(ans)


# Alternative implementation without lru_cache (for custom memoization)
def solve_manual_memo():
    """
    Manual memoization version for better control
    """
    n, m = map(int, input().split())
    digits = list(map(int, str(n)))

    # Memoization table: dp[pos][last][sum_val][tight]
    # Use dictionary for sparse states
    from collections import defaultdict
    memo = defaultdict(int)

    def dfs(pos, last, sum_val, tight):
        if sum_val > m:
            return 0
        if pos == len(digits):
            return 1

        # Check memo
        key = (pos, last, sum_val, tight)
        if key in memo:
            return memo[key]

        res = 0
        upper = digits[pos] if tight else 9

        for d in range(upper + 1):
            new_tight = tight and (d == upper)

            if last == 10:
                if d == 0:
                    res += dfs(pos + 1, 10, 0, new_tight)
                else:
                    res += dfs(pos + 1, d, 0, new_tight)
            else:
                new_sum = sum_val + abs(d - last)
                res += dfs(pos + 1, d, new_sum, new_tight)

        memo[key] = res
        return res

    print(dfs(0, 10, 0, True))


if __name__ == "__main__":
    solve()
