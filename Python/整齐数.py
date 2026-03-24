from functools import lru_cache

def solve():
    n, m = map(int, input().split())
    
    # 将n转换为数字列表
    digits = list(map(int, str(n)))
    
    @lru_cache(maxsize=None)
    def dfs(pos, last, sum_val, tight):
        """
        pos: 当前处理的位置
        last: 上一位数字 (0-9, 10表示还没有数字，即前导零状态)
        sum_val: 当前累计的差值和
        tight: 是否受限制
        """
        # 如果累计和已经超过m，直接返回0
        if sum_val > m:
            return 0
        
        # 处理完所有位
        if pos == len(digits):
            # 注意：0也是合法的非负整数
            return 1
        
        res = 0
        # 确定当前位能填的最大数字
        upper = digits[pos] if tight else 9
        
        for d in range(upper + 1):
            new_tight = tight and (d == upper)
            
            if last == 10:  # 前导零状态，这是第一位有效数字
                if d == 0:
                    # 继续前导零状态
                    res += dfs(pos + 1, 10, 0, new_tight)
                else:
                    # 第一个非零数字，差值和仍为0
                    res += dfs(pos + 1, d, 0, new_tight)
            else:
                # 计算新的差值和
                new_sum = sum_val + abs(d - last)
                res += dfs(pos + 1, d, new_sum, new_tight)
        
        return res
    
    ans = dfs(0, 10, 0, True)
    print(ans)

solve()
