n = int(input())
m = list(map(int, input().split()))

ans = 0
for i in range(1, n):
    if m[i-1] > m[i]:
        # 需要找到最小的 k，使得 m[i] * 2^k >= m[i-1]
        a, b = m[i-1], m[i]
        
        # 使用 bit_length 直接计算 k
        # k = ceil(log2(a / b))
        # bit_length 返回二进制表示的位数（不包括符号位）
        # 对于正整数 x，bit_length = floor(log2(x)) + 1
        
        # 我们需要找到最小的 k 使得 b * 2^k >= a
        # 即 2^k >= a / b
        # k >= log2(a/b)
        
        # 方法：比较 a-1 和 b 的 bit_length
        # (a-1).bit_length() 约等于 floor(log2(a-1)) + 1
        # b.bit_length() 约等于 floor(log2(b)) + 1
        
        k = (a - 1).bit_length() - b.bit_length()
        # 验证 b << k 是否 >= a
        if b << k < a:
            k += 1
        
        ans += k
        m[i] = b << k

print(ans)
