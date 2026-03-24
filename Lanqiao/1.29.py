import math

def get_prime_factors(n):
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return list(factors)

def count_coprime(n, factors):
    """
    计算 [1, n] 中与 S (其质因数为 factors) 互质的数的个数。
    使用容斥原理。
    """
    if n == 0:
        return 0
    
    m = len(factors)
    count = 0
    
    # 容斥原理：
    # 总数 - (被1个质因数整除) + (被2个质因数整除) - ...
    # 改为：计算与 S *不互质* 的数的个数，用 n 减去它
    # 或者直接计算互质的： sum_{d|P, d square-free} mu(d) * floor(n/d)
    # 这里 factors 是 S 的所有质因数 p1, p2...
    # 我们遍历所有子集
    
    for i in range(1 << m):
        divisor = 1
        set_bits = 0
        for j in range(m):
            if (i >> j) & 1:
                divisor *= factors[j]
                set_bits += 1
        
        if set_bits % 2 == 1:
            count -= n // divisor
        else:
            count += n // divisor
            
    return count

def solve():
    count_pairs = 0
    MAX_VAL = 10**6
    
    # S = a + b, S 是 2025 的倍数
    # S = 2025 * k
    # a + b = S  => b = S - a
    # 1 <= a < b <= 10^6
    # 1 <= a < S - a <= 10^6
    
    # 条件1: a < S - a  =>  2a < S  =>  a <= (S - 1) // 2
    # 条件2: S - a <= 10^6 => a >= S - 10^6
    # 条件3: a >= 1
    
    # 所以 a 的范围是 [max(1, S - 10^6), (S - 1) // 2]
    
    max_k = (2 * MAX_VAL) // 2025 + 1
    
    for k in range(1, max_k + 1):
        S = k * 2025
        if S <= 2: # a < b, so a+b >= 3 is implied typically but 1+2=3. min S is 2025 so S > 2 holds.
            continue
            
        lower_bound = max(1, S - MAX_VAL)
        upper_bound = (S - 1) // 2
        
        if lower_bound > upper_bound:
            continue
            
        # gcd(a, b) = 1 <=> gcd(a, S - a) = 1 <=> gcd(a, S) = 1
        # 我们需要在 [lower_bound, upper_bound] 范围内找与 S 互质的 a 的个数
        
        factors = get_prime_factors(S)
        
        # count in [1, upper_bound] - count in [1, lower_bound - 1]
        cnt = count_coprime(upper_bound, factors) - count_coprime(lower_bound - 1, factors)
        count_pairs += cnt
        
    print(count_pairs)

if __name__ == "__main__":
    solve()
