import sys

t = int(sys.stdin.readline())
out_lines = []
for _ in range(t):
    n, k, m = map(int, sys.stdin.readline().split())
    if k > m:
        out_lines.append("NO")
    else:
        out_lines.append("YES")
        # 构造: 每 k 个一组, [1, 1, ..., 1, m-(k-1)]
        block = ['1'] * (k - 1) + [str(m - (k - 1))]
        full_blocks, rem = divmod(n, k)
        arr = block * full_blocks + block[:rem]
        out_lines.append(' '.join(arr))
sys.stdout.write('\n'.join(out_lines))
