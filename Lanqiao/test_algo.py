
import sys

def solve_local(data):
    n = len(data)
    a = data
    
    # 计数器
    c = {}
    p = {}
    ans = 0
    
    for val in a:
        val_minus_1 = val - 1
        val_minus_2 = val - 2
        
        if c.get(val_minus_1, 0) > 0:
            c[val_minus_1] -= 1
            p[val] = p.get(val, 0) + 1
            ans += 1
        elif p.get(val_minus_1, 0) > 0:
            p[val_minus_1] -= 1
            p[val] = p.get(val, 0) + 1
            c[val_minus_2] = c.get(val_minus_2, 0) + 1
        else:
            c[val] = c.get(val, 0) + 1
            
    return ans

def test():
    # Case 1: Sample
    # 6
    # 2 1 3 6 4 7
    d1 = [2, 1, 3, 6, 4, 7]
    print(f"Case 1: Expect 2. Got {solve_local(d1)}")

    # Case 2: 1 2 3 2
    # Expect 2: (2,3) and (1,2)
    d2 = [1, 2, 3, 2]
    print(f"Case 2: Expect 2. Got {solve_local(d2)}")

    # Case 3: 4 5 6 3 4 5
    # Expect 3
    d3 = [4, 5, 6, 3, 4, 5]
    print(f"Case 3: Expect 3. Got {solve_local(d3)}")
    
    # Case 4: 1 2 3
    # Expect 1
    d4 = [1, 2, 3]
    print(f"Case 4: Expect 1. Got {solve_local(d4)}")

if __name__ == '__main__':
    test()
