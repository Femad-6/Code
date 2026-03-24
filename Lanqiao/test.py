import sys

# 设置递归深度，虽非必须但习惯性防止溢出
sys.setrecursionlimit(2000)

def solve():
    # 使用快速 I/O 读取所有输入
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
        
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
    except StopIteration:
        return

    # 将所有下标按照生成的序列大小进行分类
    small_indices = []   # 生成较小序列的下标
    large_indices = []   # 生成较大序列的下标
    neutral_indices = [] # 数组末尾无法判断的下标
    
    i = 0
    while i < N:
        # 找到连续相同的数字块，例如 [2, 2, 2, ...]
        j = i + 1
        while j < N and A[j] == A[i]:
            j += 1
            
        # 当前块的下标范围是 [i, j-1]
        current_block = list(range(i, j))
        
        if j < N:
            # 如果后面还有数字，比较当前块数字和下一个数字
            if A[i] < A[j]:
                # 当前数字比后面小 -> 属于 Small 组
                small_indices.extend(current_block)
            else:
                # 当前数字比后面大 -> 属于 Large 组
                large_indices.extend(current_block)
        else:
            # 已经是数组末尾 -> 属于 Neutral 组
            neutral_indices.extend(current_block)
            
        i = j

    # 确定第 K 个序列对应的原始下标
    # 逻辑顺序：Small组 -> Neutral组 -> Large组(逆序)
    
    len_small = len(small_indices)
    len_neutral = len(neutral_indices)
    
    target_idx = -1
    
    if K <= len_small:
        # 在 Small 组中，顺序就是下标从小到大
        target_idx = small_indices[K-1]
    elif K <= len_small + len_neutral:
        # 在 Neutral 组中
        target_idx = neutral_indices[K - 1 - len_small]
    else:
        # 在 Large 组中，顺序是下标从大到小（逆序）
        # 我们需要找到从后往前数的第 remaining_k 个元素
        remaining_k = K - len_small - len_neutral
        target_idx = large_indices[len(large_indices) - remaining_k]

    # 构造输出：在 target_idx 位置插入一个副本
    # 即：A[0...target_idx] + A[target_idx] + A[target_idx+1...N]
    
    output = []
    # 转换为字符串以便快速输出
    # 1. 输出前半部分（包含 target_idx）
    for idx in range(target_idx + 1):
        output.append(str(A[idx]))
    # 2. 输出克隆的细胞
    output.append(str(A[target_idx])) 
    # 3. 输出后半部分
    for idx in range(target_idx + 1, N):
        output.append(str(A[idx]))
        
    sys.stdout.write(" ".join(output) + "\n")

if __name__ == '__main__':
    solve()