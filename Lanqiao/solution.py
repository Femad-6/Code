import sys

# Increases the recursion depth to handle deep trees
sys.setrecursionlimit(2000)

def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        
        weights = []
        for _ in range(n):
            weights.append(int(next(iterator)))
            
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u = int(next(iterator))
            v = int(next(iterator))
            adj[u].append(v)
            adj[v].append(u)
            
    except StopIteration:
        return

    MOD = 10**9 + 7
    ans = 0
    
    # dp[u][s] will be returned by dfs, representing counts for subgraphs rooted at u
    
    def dfs(u, p):
        nonlocal ans
        
        # Initialize dp array for current node u.
        # current_dp[s] = number of connected subgraphs rooted at u with sum s.
        current_dp = [0] * (k + 1)
        w = weights[u-1]
        
        if w <= k:
            current_dp[w] = 1
        
        # Optimization: keep track of the max sum currently reachable in current_dp to bounding loops
        # though with K=100, simple bounds are also fine.
        
        for v in adj[u]:
            if v == p:
                continue
            
            child_dp = dfs(v, u)
            
            # Temporary array for the convolution result (P_u * P_v)
            # We want to add P_u * P_v to the existing P_u
            # effectively P_u_new = P_u * (1 + P_v)
            
            # We calculate `convolved = P_u * P_v` and then `current_dp += convolved`
            
            # To optimize, we can use a temporary buffer just for the updates
            # Or simpler: build a completely new array for the next state
            new_dp = [0] * (k + 1)
            
            # Copy existing ways (corresponds to multiplying by 1)
            for i in range(k + 1):
                new_dp[i] = current_dp[i]
                
            # Add convolution (corresponds to multiplying by P_v)
            for x in range(k + 1):
                if current_dp[x] == 0:
                    continue
                # We only need to iterate y such that x + y <= k
                for y in range(k + 1 - x):
                    if child_dp[y] == 0: 
                        continue
                    
                    added_ways = (current_dp[x] * child_dp[y]) % MOD
                    new_dp[x + y] = (new_dp[x + y] + added_ways) % MOD
            
            current_dp = new_dp

        # Add to global answer
        ans = (ans + current_dp[k]) % MOD
        return current_dp

    dfs(1, -1)
    print(ans)

if __name__ == '__main__':
    solve()
