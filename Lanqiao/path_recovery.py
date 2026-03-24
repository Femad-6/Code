import sys

# Increase limits
sys.setrecursionlimit(2000)

def solve():
    # Read all input
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        s = next(iterator)
    except StopIteration:
        return

    MOD = 10**9 + 7
    
    # dp[g][h] stores the number of ways
    # g = current min_height (L)
    # h = (max_height - min_height) / 2
    # We use a dictionary to store sparse states: key=(g, h), value=count
    current_dp = {(0, 0): 1}
    
    for char in s:
        next_dp = {}
        
        # Helper to add to next_dp
        def add(g, h, count):
            if h < 0: return
            state = (g, h)
            next_dp[state] = (next_dp.get(state, 0) + count) % MOD

        for (g, h), count in current_dp.items():
            # Transitions derived:
            # U: (g, h) -> (g+1, h)
            # D: if g==0 -> (1, h-1); if g>0 -> (g-1, h)
            # F: if g==0 -> (1, h);   if g>0 -> (g-1, h+1)
            
            # 1. Try 'U'
            if char == 'U' or char == '*' or char == 'F': 
                # Note: 'F' in input means Free segment, which can be U or D.
                # The problem says 'F' is Free. 'U', 'D' are fixed. '*' is blurred.
                # So if char is 'F', we sum U-transition and D-transition.
                # If char is '*', we sum U, D, F transitions (where F is U or D choices).
                # Wait. Input chars are U, D, F, *.
                # '*' becomes U, D, or F.
                # If * becomes F, that F can be anything.
                # So * -> U, * -> D, * -> F.
                # Effectively:
                # * -> U
                # * -> D
                # * -> F -> acts like Union of paths.
                
                # Careful: The problem asks for number of ways to REPLACE '*'.
                # A replacement results in a string T.
                # T is feasible if...
                # So we are counting T's.
                pass

            # Let's map choices correctly.
            # If s[i] == 'U': We MUST do U-logic.
            # If s[i] == 'D': We MUST do D-logic.
            # If s[i] == 'F': We MUST do F-logic (Union logic).
            # If s[i] == '*': We can choose to simplify it to 'U', 'D', or 'F'.
            #   Choice 1: Replace with 'U'. dynamics = U-logic.
            #   Choice 2: Replace with 'D'. dynamics = D-logic.
            #   Choice 3: Replace with 'F'. dynamics = F-logic.
            
            # U-logic:
            # (g+1, h)
            
            # D-logic:
            # if g == 0: (1, h-1)
            # else: (g-1, h)
            
            # F-logic:
            # if g == 0: (1, h)
            # else: (g-1, h+1)
            
            # Applying based on char
            if char == 'U':
                add(g + 1, h, count)
                
            elif char == 'D':
                if g == 0:
                    add(1, h - 1, count)
                else:
                    add(g - 1, h, count)
                    
            elif char == 'F':
                if g == 0:
                    add(1, h, count)
                else:
                    add(g - 1, h + 1, count)
                    
            elif char == '*':
                # Option 1: become U
                add(g + 1, h, count)
                
                # Option 2: become D
                if g == 0:
                    add(1, h - 1, count)
                else:
                    add(g - 1, h, count)
                    
                # Option 3: become F
                if g == 0:
                    add(1, h, count)
                else:
                    add(g - 1, h + 1, count)
                    
        current_dp = next_dp

    # Final answer: Sum of counts where g=0 (L=0)
    ans = 0
    for (g, h), count in current_dp.items():
        if g == 0:
            ans = (ans + count) % MOD
            
    print(ans)

if __name__ == '__main__':
    solve()
