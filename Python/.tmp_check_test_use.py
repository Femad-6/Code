import subprocess
import sys
from collections import deque


def brute(a, b, c):
    q = deque([(a, 0)])
    vis = {a}
    while q:
        x, d = q.popleft()
        if x == b:
            return d
        for mv in (1, 2):
            y = x + mv
            if y > b:
                continue
            if y % c == 0:
                continue
            if y not in vis:
                vis.add(y)
                q.append((y, d + 1))
    return -1

for c in range(2, 25):
    for a in range(1, 80):
        if a % c == 0:
            continue
        for b in range(a, 160):
            if b % c == 0:
                continue
            inp = f"{a} {b} {c}\n".encode()
            out = subprocess.check_output([
                "d:/Python/python.exe",
                "d:/Code/Python/Test_use.py",
            ], input=inp).decode().strip()
            ans = int(out)
            br = brute(a, b, c)
            if ans != br:
                print("mismatch", a, b, c, ans, br)
                sys.exit(0)

print("ok")
