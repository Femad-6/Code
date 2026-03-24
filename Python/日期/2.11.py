n = int(input())
a = list(map(int, input().split()))

ans = 0

for i in range(n // 2):
    j = n - 1 - i
    diff = a[j] - a[i]
    
    if i + 1 < j:
        inner_diff = a[j - 1] - a[i + 1]
        
        # 同号时，用操作1帮助内层
        if diff * inner_diff > 0:
            x = min(abs(diff), abs(inner_diff))
        else:
            x = 0
        
        ans += abs(diff)
        a[i + 1] += (1 if diff > 0 else -1) * x
    else:
        ans += abs(diff)

print(ans)