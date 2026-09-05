n, m, k = map(int, input().split())
a = list(map(int, input().split()))

top = m * k
pairs = sorted(zip(a, range(n)), reverse=True)[:top]  # 前 m*k 大的元素（含下标）
ans = sum(v for v, _ in pairs)
chosen = {i for _, i in pairs}

cuts = []
cnt = 0
for i in range(n - 1):
    if i in chosen:
        cnt += 1
    if cnt == m and len(cuts) < k - 1:  # 每段正好凑够 m 个标记就切一刀
        cuts.append(i + 1)
        cnt = 0

print(ans)
print(*cuts)
