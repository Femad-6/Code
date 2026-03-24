from collections import Counter

n = int(input())
a = list(map(int, input().split()))

# 统计每个数字中'6'的个数，上限为6（因为超过6也按6算）
counts = []
for num in a:
    c = str(num).count('6')
    counts.append(min(c, 6))

# 按6的个数分类
cnt = [0] * 7
for c in counts:
    cnt[c] += 1

ans = 0

# 优先处理高数量的
# 6单独成组
ans += cnt[6]
cnt[6] = 0

# 尽可能凑组，每组和>=6，最多3个数
# 从大到小贪心凑
def make_group():
    global ans
    # 尝试所有可能的组合
    # 两个数
    for i in range(6, 0, -1):
        for j in range(i, -1, -1):
            if i + j >= 6 and cnt[i] > 0 and cnt[j] > 0:
                if i == j:
                    if cnt[i] >= 2:
                        cnt[i] -= 2
                        ans += 1
                        return True
                else:
                    cnt[i] -= 1
                    cnt[j] -= 1
                    ans += 1
                    return True
    
    # 三个数
    for i in range(6, 0, -1):
        for j in range(i, -1, -1):
            for k in range(j, -1, -1):
                if i + j + k >= 6 and cnt[i] > 0 and cnt[j] > 0 and cnt[k] > 0:
                    if i == j == k:
                        if cnt[i] >= 3:
                            cnt[i] -= 3
                            ans += 1
                            return True
                    elif i == j:
                        if cnt[i] >= 2 and cnt[k] > 0:
                            cnt[i] -= 2
                            cnt[k] -= 1
                            ans += 1
                            return True
                    elif j == k:
                        if cnt[i] > 0 and cnt[j] >= 2:
                            cnt[i] -= 1
                            cnt[j] -= 2
                            ans += 1
                            return True
                    else:
                        cnt[i] -= 1
                        cnt[j] -= 1
                        cnt[k] -= 1
                        ans += 1
                        return True
    return False

while make_group():
    pass

print(ans)