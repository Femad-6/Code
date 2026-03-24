def sieve_of_eratosthenes(n):
    if n < 2:
        return 0
    is_prime = [True] * (n + 1)
    is_prime[0], is_prime[1] = False, False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return sum(is_prime)

# 测试埃拉托斯特尼筛法
import time

n = 10**6  # 可以根据需要调整n的大小
start_time = time.time()
result_sieve = sieve_of_eratosthenes(n)
end_time = time.time()

print(f"埃拉托斯特尼筛法结果: {result_sieve}, 耗时: {end_time - start_time}秒")


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def count_primes_trial_division(n):
    count = 0
    for i in range(2, n + 1):
        if is_prime(i):
            count += 1
    return count

# 测试简单质数测试
start_time = time.time()
result_trial = count_primes_trial_division(n)
end_time = time.time()

print(f"简单质数测试结果: {result_trial}, 耗时: {end_time - start_time}秒")
