import sys

# 设置递归深度
sys.setrecursionlimit(200000)

def solve():
    # 读取输入
    try:
        input_data = sys.stdin.read().split()
    except Exception:
        return
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n_str = next(iterator)
        n = int(n_str)
    except StopIteration:
        return

    # 题目约定 a_i <= 10^6
    # 使用数组代替字典，提高访问速度并减少内存开销
    # 大小设为 1000005 足够
    MAX_VAL = 1000005
    c = [0] * MAX_VAL
    p = [0] * MAX_VAL
    ans = 0
    
    for _ in range(n):
        try:
            val_str = next(iterator)
            if not val_str: break 
            val = int(val_str)
        except StopIteration:
            break
            
        val_minus_1 = val - 1
        val_minus_2 = val - 2
        
        # 优化: 尽量减少 list 索引查找
        # 1. 尝试匹配空闲的 prev (val-1)
        # val >= 1. 访问 c[val-1] 安全 (val-1 >= 0)
        if c[val_minus_1] > 0:
            c[val_minus_1] -= 1
            p[val] += 1
            ans += 1
        # 2. 尝试从已有的配对 (val-2, val-1) 中"偷"一个 val-1
        elif p[val_minus_1] > 0:
            p[val_minus_1] -= 1
            p[val] += 1
            # val-2 可能是 -1. c[-1] 修改数组末尾. 
            # 只要不再读取 c[MAX_VAL-1], 这是安全的.
            c[val_minus_2] += 1
        # 3. 无法匹配，加入空闲池
        else:
            c[val] += 1
            
    print(ans)

if __name__ == '__main__':
    solve()
