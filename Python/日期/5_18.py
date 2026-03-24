import sys

def main():
    data = sys.stdin.read().split()
    ptr = 0
    n = int(data[ptr])
    ptr += 1
    m = int(data[ptr])
    ptr += 1
    k = int(data[ptr])
    ptr += 1

    # 初始化矩阵F，从1开始索引
    F = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            F[i][j] = int(data[ptr])
            ptr += 1

    # 计算前缀平方和数组
    sum_sq = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sum_sq[i][j] = F[i][j] ** 2 + sum_sq[i - 1][j] + sum_sq[i][j - 1] - sum_sq[i - 1][j - 1]

    q = int(data[ptr])
    ptr += 1

    res = []
    for _ in range(q):
        x = int(data[ptr])
        ptr += 1
        y = int(data[ptr])
        ptr += 1
        x2 = x + k - 1
        y2 = y + k - 1
        # 计算区域平方和
        current = sum_sq[x2][y2] - sum_sq[x - 1][y2] - sum_sq[x2][y - 1] + sum_sq[x - 1][y - 1]
        res.append(str(current))
    
    print('\n'.join(res))

if __name__ == "__main__":
    main()