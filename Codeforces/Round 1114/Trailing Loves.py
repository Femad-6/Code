n, b = map(int, input().split())

# 分解 b 的质因数
factors = []
x = b
d = 2
while d * d <= x:
    if x % d == 0:
        e = 0
        while x % d == 0:
            x //= d
            e += 1
        factors.append((d, e))
    d += 1
if x > 1:
    factors.append((x, 1))

# 答案 = min(v_p(n!) // e)，v_p(n!) 用勒让德公式
ans = float('inf')
for p, e in factors:
    cnt = 0
    y = n
    while y:
        y //= p
        cnt += y
    ans = min(ans, cnt // e)

print(ans)
