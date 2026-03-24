MOD = 10**9 + 7


def is_coprime(a: int, b: int) -> bool:
	if a == 1 or b == 1:
		return True
	if a == b:
		return False
	return True


def mat_mul(a, b):
	n = len(a)
	m = len(b[0])
	k = len(b)
	res = [[0] * m for _ in range(n)]
	for i in range(n):
		for t in range(k):
			if a[i][t] == 0:
				continue
			ait = a[i][t]
			for j in range(m):
				if b[t][j] == 0:
					continue
				res[i][j] = (res[i][j] + ait * b[t][j]) % MOD
	return res


def mat_pow(mat, exp: int):
	size = len(mat)
	res = [[0] * size for _ in range(size)]
	for i in range(size):
		res[i][i] = 1
	base = mat
	while exp > 0:
		if exp & 1:
			res = mat_mul(res, base)
		base = mat_mul(base, base)
		exp >>= 1
	return res


def solve(n: int) -> int:
	values = [1, 5, 6]

	states = []
	for top in values:
		for bottom in values:
			if is_coprime(top, bottom):
				states.append((top, bottom))

	s = len(states)  # 7 个合法列状态

	trans = [[0] * s for _ in range(s)]
	for i in range(s):
		a_top, a_bottom = states[i]
		for j in range(s):
			b_top, b_bottom = states[j]
			if is_coprime(a_top, b_top) and is_coprime(a_bottom, b_bottom):
				trans[i][j] = 1

	if n == 1:
		return s

	p = mat_pow(trans, n - 1)

	# 初始向量 init = [1,1,...,1]，答案是 init * p 的所有元素和
	ans = 0
	for j in range(s):
		col_sum = 0
		for i in range(s):
			col_sum = (col_sum + p[i][j]) % MOD
		ans = (ans + col_sum) % MOD
	return ans


def solve_linear(n: int) -> int:
	values = [1, 5, 6]

	states = []
	for top in values:
		for bottom in values:
			if is_coprime(top, bottom):
				states.append((top, bottom))

	s = len(states)
	trans = [[0] * s for _ in range(s)]
	for i in range(s):
		a_top, a_bottom = states[i]
		for j in range(s):
			b_top, b_bottom = states[j]
			if is_coprime(a_top, b_top) and is_coprime(a_bottom, b_bottom):
				trans[i][j] = 1

	dp = [1] * s
	for _ in range(n - 1):
		ndp = [0] * s
		for i in range(s):
			if dp[i] == 0:
				continue
			for j in range(s):
				if trans[i][j]:
					ndp[j] = (ndp[j] + dp[i]) % MOD
		dp = ndp

	return sum(dp) % MOD


if __name__ == "__main__":
	n = int(input().strip())
	print(solve(n))
