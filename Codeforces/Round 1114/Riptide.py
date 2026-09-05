t = int(input())
for _ in range(t):
    x = sorted(map(int, input().split()))
    rounds = 0
    while x[0] < x[1] < x[2]:  # 三人 token 全部不同 -> 游戏继续
        x[0] += 1  # 最少者 +1
        x[2] -= 1  # 最多者 -1
        x.sort()
        rounds += 1
    print(rounds)
