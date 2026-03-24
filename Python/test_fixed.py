def solve():
    N = int(input())
    
    # 特殊情况：N在两位数范围内
    if N <= 45:
        return find_two_digit(N)
    
    # 计算各长度的数字个数
    N -= 45  # 减去两位数的数量
    
    length = 3  # 从3位数开始
    cnt = 225  # 3位数的数量
    
    while N > cnt:
        N -= cnt
        length += 1
        cnt *= 5
    
    # 现在 N 是在 length 位数中的第 N 个
    return find_kth(length, N)


def find_two_digit(N):
    """找到第N个两位奇偶交替数字"""
    # 按数值顺序：10-99
    # 遍历十位 1-9，对于每个十位，遍历符合条件的个位
    
    count = 0
    for ten in range(1, 10):  # 十位 1-9
        ten_is_odd = ten % 2 == 1
        for one in range(0, 10):  # 个位 0-9
            one_is_odd = one % 2 == 1
            if ten_is_odd != one_is_odd:  # 奇偶性不同
                count += 1
                if count == N:
                    return ten * 10 + one


def find_kth(length, N):
    """找到 length 位数的第 N 个奇偶交替数字"""
    # 按字典序（数值顺序）构造
    # 使用DFS或迭代方法，按顺序枚举
    
    odd_digits = [1, 3, 5, 7, 9]
    even_digits = [0, 2, 4, 6, 8]
    all_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # 计算以某个前缀开头的数字个数
    def count_with_prefix(prefix, prev_is_odd, remaining_len):
        """计算以prefix为前缀，还剩remaining_len位的奇偶交替数字个数"""
        if remaining_len == 0:
            return 1
        # 下一位必须和prev_is_odd奇偶性不同
        return 5 ** remaining_len
    
    # 确定第一位（不能为0）
    result = 0
    for first in range(1, 10):  # 1-9
        first_is_odd = first % 2 == 1
        # 计算以first开头的数字个数
        cnt = 5 ** (length - 1)
        
        if N > cnt:
            N -= cnt
        else:
            result = first
            prev_is_odd = first_is_odd
            break
    
    # 确定后续位
    for pos in range(length - 1):
        for digit in range(0, 10):
            digit_is_odd = digit % 2 == 1
            # 必须和前一位奇偶性不同
            if digit_is_odd == prev_is_odd:
                continue
            
            cnt = 5 ** (length - pos - 2) if length - pos - 2 >= 0 else 1
            
            if N > cnt:
                N -= cnt
            else:
                result = result * 10 + digit
                prev_is_odd = digit_is_odd
                break
    
    return result


print(solve())
