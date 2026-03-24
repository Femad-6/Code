mod = 998244353

def mat_mult(A, B):
    """2x2矩阵乘法"""
    return [
        [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % (mod-1), 
         (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % (mod-1)],
        [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % (mod-1), 
         (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % (mod-1)]
    ]

def mat_pow(M, n):
    """矩阵快速幂"""
    if n == 0:
        return [[1, 0], [0, 1]]
    if n == 1:
        return M
    half = mat_pow(M, n // 2)
    res = mat_mult(half, half)
    if n % 2 == 1:
        res = mat_mult(res, M)
    return res

def fib(n):
    """计算第n个斐波那契数 F_n，其中 F_0=0, F_1=1"""
    if n == 0:
        return 0
    M = [[1, 1], [1, 0]]
    return mat_pow(M, n)[0][1]

def power(a, b):
    """快速幂 a^b % mod"""
    res = 1
    a = a % mod
    while b > 0:
        if b & 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1
    return res

n = int(input())

if n == 1:
    print(2)
else:
    # G_i = 2^F_{i-1} * 3^F_i
    # 前n项乘积 = 2^{sum(F_{i-1})} * 3^{sum(F_i)} for i=0 to n-1
    # sum(F_i, i=0 to n-1) = F_{n+1} - 1
    # sum(F_{i-1}, i=0 to n-1) = sum(F_i, i=-1 to n-2) = F_n - 1 + F_{-1}，需要仔细算
    
    # 实际上：G_0 = 2 = 2^1 * 3^0, G_1 = 3 = 2^0 * 3^1
    # 所以 G_i 中 2 的指数是 F_{i-1} (定义 F_{-1}=1)
    # 通过验证：G_2 = 6 = 2^1 * 3^1, F_1=1, F_2=1 ✓
    
    Fn1 = fib(n + 1)      # F_{n+1}
    Fn = fib(n)           # F_n
    
    # sum_{i=0}^{n-1} F_i = F_{n+1} - 1
    # sum_{i=0}^{n-1} F_{i-1} = sum_{i=0}^{n-1} F_i + (F_{-1} - F_{n-1}) = F_{n+1} - 1 + 1 - F_{n-1} = F_{n+1} - F_{n-1} = F_n
    # 验证：n=2时，sum = F_{-1} + F_0 = 1 + 0 = 1，而 F_2 = 1 ✓
    
    exp3 = (Fn1 - 1) % (mod - 1)  # 3 的指数
    exp2 = Fn % (mod - 1)          # 2 的指数
    
    ans = power(2, exp2) * power(3, exp3) % mod
    print(ans)