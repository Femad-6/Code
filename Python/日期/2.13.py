def solve():
    n = int(input())
    for _ in range(n):
        s = input().strip()
        
        has_lower = 0  # 已有的小写字母（不含o）
        has_upper = 0  # 已有的大写字母（不含O）
        has_digit = 0  # 已有的数字（不含0）
        cnt_o = 0      # o的数量
        cnt_O = 0      # O的数量
        cnt_0 = 0      # 0的数量
        
        for c in s:
            if c == 'o':
                cnt_o += 1
            elif c == 'O':
                cnt_O += 1
            elif c == '0':
                cnt_0 += 1
            elif c.islower():
                has_lower += 1
            elif c.isupper():
                has_upper += 1
            elif c.isdigit():
                has_digit += 1
        
        # 需要补充的类型（注意：o/O/0本身也算对应类型）
        need_lower = 1 if (has_lower + cnt_o) == 0 else 0
        need_upper = 1 if (has_upper + cnt_O) == 0 else 0
        need_digit = 1 if (has_digit + cnt_0) == 0 else 0
        
        # 如果不需要任何补充，答案为0
        if need_lower == 0 and need_upper == 0 and need_digit == 0:
            print(0)
            continue
        
        # 枚举从o, O, 0中各取多少来满足需求
        # i个o变成小写, j个o变成大写, k个o变成数字 (i+j+k = cnt_o)
        # 类似地处理O和0
        
        ans = float('inf')
        
        # 枚举o的分配：变成小写的数量，变成大写的数量，变成数字的数量
        for o_to_lower in range(cnt_o + 1):
            for o_to_upper in range(cnt_o + 1 - o_to_lower):
                o_to_digit = cnt_o - o_to_lower - o_to_upper
                
                # 枚举O的分配
                for O_to_lower in range(cnt_O + 1):
                    for O_to_upper in range(cnt_O + 1 - O_to_lower):
                        O_to_digit = cnt_O - O_to_lower - O_to_upper
                        
                        # 枚举0的分配
                        for zero_to_lower in range(cnt_0 + 1):
                            for zero_to_upper in range(cnt_0 + 1 - zero_to_lower):
                                zero_to_digit = cnt_0 - zero_to_lower - zero_to_upper
                                
                                # 计算总共有多少各类字符
                                total_lower = has_lower + o_to_lower + O_to_lower + zero_to_lower
                                total_upper = has_upper + o_to_upper + O_to_upper + zero_to_upper
                                total_digit = has_digit + o_to_digit + O_to_digit + zero_to_digit
                                
                                # 检查是否满足条件
                                if total_lower >= 1 and total_upper >= 1 and total_digit >= 1:
                                    # 计算操作次数
                                    # o: 变成小写(0次)，变成大写(1次)，变成数字(1次)
                                    # O: 变成小写(1次)，变成大写(0次)，变成数字(1次)
                                    # 0: 变成小写(1次)，变成大写(1次)，变成数字(0次)
                                    ops = o_to_upper + o_to_digit  # o的操作次数
                                    ops += O_to_lower + O_to_digit  # O的操作次数
                                    ops += zero_to_lower + zero_to_upper  # 0的操作次数
                                    
                                    ans = min(ans, ops)
        
        print(ans if ans != float('inf') else -1)

solve()
