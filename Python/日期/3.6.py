def can_be_sum(N):
    k = 3
    # 当k为偶数时，最小和可以是负数；当k为奇数时，最小和也可以是负数
    # 所以我们需要检查所有可能的k
    while k <= 2 * abs(N) + 1:  # 设置一个合理的上限
        if (2 * N) % k == 0:
            m = (2 * N) // k  # m = 2a + k - 1
            # m 和 k 必须奇偶性不同（这样a才是整数）
            # 不再要求 m > k，允许a为0或负数
            if (m - k) % 2 == 1:
                a = (m - k + 1) // 2  # 首项
                # 验证：序列 a, a+1, ..., a+k-1 的和是否为N
                seq_sum = k * (2 * a + k - 1) // 2
                if seq_sum == N:
                    return True
        k += 1
    return False


N=int(input())
a=list(map(int,input().split()))

ans=0
for i in a:
    if can_be_sum(i):
        ans+=1
print(ans)
