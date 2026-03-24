---
name: algorithm求解
description: Algorithm competition problem solving with Python, including dynamic programming (tree DP, digit DP), graph algorithms, and common optimization techniques. Use when solving competitive programming problems that require efficient algorithms, state design, and careful implementation of DP transitions.
---

# Algorithm Competition Problem Solving

## Overview

This skill provides systematic approaches to solving algorithm competition problems in Python, with focus on:

- Dynamic Programming (Tree DP, Digit DP, State DP)
- Sequence DP with sliding-window minimum optimization
- Graph algorithms and tree traversals
- Common optimization patterns
- Debugging and verification techniques

## Quick Reference

### Problem Type Identification

| Problem Feature | Likely Algorithm |
|----------------|------------------|
| Counting/optimization on trees | Tree DP |
| Range queries with constraints | Digit DP |
| Select positions with bounded gap | Sequence DP + Monotonic Queue |
| Distance constraints between nodes | Graph DP / BFS |
| Large number ranges (10^18) | Digit DP with memoization |
| Independent set with distance constraints | Tree DP with state design |

### State Design Patterns

**Tree DP (3-state)**:

```python
dp[u][0]  # u not selected, parent not selected
dp[u][1]  # u not selected, parent selected
dp[u][2]  # u selected
```

**Digit DP**:

```python
dfs(pos, last_digit, current_sum, is_tight)
# pos: current position
# last_digit: previous digit (for constraint checking)
# current_sum: accumulated value
# is_tight: whether bounded by upper limit
```

**Sequence DP with bounded gap**:

```python
dp[i] = a[i] + min(dp[j])
# j is restricted to a sliding window before i
```

## Core Workflows

### 1. Tree DP Problems

**When to use**: Problems involving tree structures with constraints between parent and child nodes.

**Key insight**: The constraint between siblings (distance-2 relationship) is often the trickiest part.

**Template**:

```python
import sys
sys.setrecursionlimit(300000)
MOD = 998244353

def solve():
    n = int(input())
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    dp = [[0, 0, 0] for _ in range(n + 1)]
    
    def dfs(u, fa):
        children = [v for v in adj[u] if v != fa]
        for v in children:
            dfs(v, u)
        
        # State 1: parent selected -> children cannot be selected
        dp[u][1] = 1
        for v in children:
            dp[u][1] = dp[u][1] * dp[v][0] % MOD
        
        # State 2: u selected -> children cannot be selected
        dp[u][2] = 1
        for v in children:
            dp[u][2] = dp[u][2] * dp[v][1] % MOD
        
        # State 0: u not selected, parent not selected
        # At most one child can be selected (siblings distance=2)
        all_not = 1
        for v in children:
            all_not = all_not * dp[v][0] % MOD
        
        one_selected = 0
        for i, vi in enumerate(children):
            prod = dp[vi][2]
            for j, vj in enumerate(children):
                if i != j:
                    prod = prod * dp[vj][0] % MOD
            one_selected = (one_selected + prod) % MOD
        
        dp[u][0] = (all_not + one_selected) % MOD
    
    dfs(1, 0)
    ans = (dp[1][0] + dp[1][2] - 1) % MOD  # -1 for empty set
    print(ans)

solve()
```

### 2. Digit DP Problems

**When to use**: Counting numbers in range [0, n] satisfying digit-based constraints.

**Key insight**: Use memoization with tight constraint to handle large ranges efficiently.

**Template**:

```python
from functools import lru_cache

def solve():
    n, m = map(int, input().split())
    digits = list(map(int, str(n)))
    
    @lru_cache(maxsize=None)
    def dfs(pos, last, sum_val, tight):
        if sum_val > m:
            return 0
        if pos == len(digits):
            return 1
        
        res = 0
        upper = digits[pos] if tight else 9
        
        for d in range(upper + 1):
            new_tight = tight and (d == upper)
            
            if last == 10:  # Leading zero state
                if d == 0:
                    res += dfs(pos + 1, 10, 0, new_tight)
                else:
                    res += dfs(pos + 1, d, 0, new_tight)
            else:
                new_sum = sum_val + abs(d - last)
                res += dfs(pos + 1, d, new_sum, new_tight)
        
        return res
    
    print(dfs(0, 10, 0, True))

solve()
```

### 3. Sequence DP with Gap Constraints

**When to use**: Choose several positions in an array, usually with fixed endpoints or mandatory picks, and adjacent chosen positions must satisfy a maximum distance or maximum number of skipped elements.

**Key insight**: Convert the constraint into a bound on index difference. Then define DP on the last chosen position and optimize the sliding minimum with a monotonic queue.

**Typical transformation**:

- If the problem says there can be at most `k` unchosen elements between adjacent chosen positions, then for positions `j < i`:
- `i - j - 1 <= k`
- equivalent to `i - j <= k + 1`

**State design**:

```python
dp[i] = minimum total cost when position i is chosen as black / selected
```

**Transition**:

```python
dp[i] = a[i] + min(dp[j])
# j in [i - k - 1, i - 1]
```

If `1` and `n` must be selected, then:

```python
dp[1] = a[1]
answer = dp[n]
```

**Complexity**:

- Naive transition: `O(nk)`
- With monotonic queue for sliding-window minimum: `O(n)`

**Template**:

```python
from collections import deque

def solve():
    n, k = map(int, input().split())
    a = [0] + list(map(int, input().split()))

    dp = [0] * (n + 1)
    dp[1] = a[1]

    q = deque([1])  # indices with increasing dp values

    for i in range(2, n + 1):
        left = i - k - 1

        while q and q[0] < left:
            q.popleft()

        dp[i] = dp[q[0]] + a[i]

        while q and dp[q[-1]] >= dp[i]:
            q.pop()

        q.append(i)

    print(dp[n])

solve()
```

**Checklist**:

- Clarify whether the constraint is on skipped count or index distance
- Check whether endpoints are mandatory
- Confirm whether the objective is min-cost, max-value, or counting
- If the transition asks for min/max over a contiguous previous range, consider monotonic queue immediately

## Common Pitfalls

### State Transition Errors

**Problem**: Sibling constraints in tree DP

- **Symptom**: Answer too large (counting invalid configurations)
- **Cause**: Allowing multiple children to be selected when they should be mutually exclusive
- **Fix**: Explicitly enforce "at most one child selected" constraint

**Problem**: Parent-child state mismatch

- **Symptom**: Answer too small or incorrect
- **Cause**: Child enters wrong state based on parent's condition
- **Fix**: Carefully track what each state means and verify transitions

**Problem**: Gap constraint translated incorrectly

- **Symptom**: Off-by-one errors, especially sample mismatch
- **Cause**: Mixing up "at most k white elements" with "distance at most k"
- **Fix**: Write the exact equivalence first: if white count is `k`, then index gap is `k + 1`

**Problem**: Sliding window boundary incorrect

- **Symptom**: DP seems correct on small random tests but fails near boundaries
- **Cause**: Using `[i-k, i-1]` instead of `[i-k-1, i-1]`, or popping valid states too early
- **Fix**: Derive the legal predecessor interval before coding the queue maintenance

### Boundary Conditions

**Always check**:

- n = 0, n = 1 (minimal cases)
- Leaf nodes in tree DP
- Root node special handling (no parent)
- Empty set exclusion when required

### Implementation Details

**Recursion depth**: Always set `sys.setrecursionlimit(300000)` for tree problems
**Modulo operations**: Use `(ans + MOD) % MOD` for negative results
**Input parsing**: Use `list(map(int, input().split()))` for multiple integers

## Debugging Techniques

### 1. Small Case Verification

Manually compute DP values for small trees:

```python
# Add debug output
print(f"Node {u}: dp = {dp[u]}")
```

### 2. State Transition Tracing

For complex transitions, add step-by-step logging:

```python
print(f"  Processing child {v}")
print(f"  Before: dp[{u}] = {dp[u]}")
print(f"  Child dp: {dp[v]}")
# ... update ...
print(f"  After: dp[{u}] = {dp[u]}")
```

### 3. Brute Force Comparison

For small n, implement brute force to verify DP:

```python
def brute_force(n, edges):
    # Try all subsets and check constraints
    from itertools import combinations
    # ... implementation
```

## Advanced Patterns

### Handling Multiple Constraints

When problem has multiple interacting constraints:

1. Identify the primary constraint for state design
2. Handle secondary constraints in transitions
3. Consider adding more state dimensions if needed

### Optimization Techniques

**Prefix/Suffix products**: For "at most one" constraints, use prefix/suffix products to achieve O(n) instead of O(n²)

**State compression**: When state space is large but sparse, use dictionaries instead of arrays

**Iterative DFS**: Convert recursive DFS to iterative using explicit stack when recursion depth is a concern

## Example Problems

### Tree DP: Distance-2 Independent Set

**Problem**: Select nodes such that any two selected nodes have distance > 2.

**Key insight**: If u is not selected, at most one child can be selected (siblings have distance 2).

**Solution**: See Tree DP template above.

### Digit DP: Adjacent Digit Constraints

**Problem**: Count numbers where sum of absolute differences between adjacent digits ≤ m.

**Key insight**: Need to track last digit and current sum in state.

**Solution**: See Digit DP template above.

### Sequence DP: Minimum Black Sum with Bounded Gaps

**Problem**: Initially only the first and last positions are chosen. You may choose more positions so that adjacent chosen positions contain at most `k` unchosen elements, and the total chosen sum is minimized.

**Key insight**: Let `dp[i]` be the minimum sum when position `i` is chosen. Then `dp[i] = a[i] + min(dp[j])` over the previous legal window, which is exactly a sliding-window minimum problem.

**Solution**: Use DP plus a monotonic queue in `O(n)`.

## References

- See `scripts/tree_dp_template.py` for complete tree DP implementation
- See `scripts/digit_dp_template.py` for complete digit DP implementation
data = list(map(int, input().split()))

```

## 总结

解决算法竞赛题目的关键：
1. **彻底理解题意**，不要急于编码
2. **设计清晰的状态**，考虑所有约束
3. **从小样例验证**，确保逻辑正确
4. **注意边界情况**，避免低级错误
5. **代码结构清晰**，便于调试和修改

记住：好的算法设计比代码技巧更重要！