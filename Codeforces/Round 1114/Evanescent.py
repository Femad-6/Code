t = int(input())
for _ in range(t):
    n = int(input())
    s = input()
    runs = 1 + sum(1 for i in range(1, n) if s[i] != s[i - 1])
    best = 0
    for i in range(1, n - 1):
        if s[i - 1] == s[i + 1]:
            if s[i] != s[i - 1]:  # aba 型：删除中间字符，两端 run 合并，减 2
                best = 2
                break
        elif s[i - 1] != s[i] and s[i] != s[i + 1]:  # 三者全不同：删除后该 run 消失，减 1
            best = 1
    print(runs - best)
