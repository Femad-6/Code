import sys

# Increase recursion depth just in case, though not strictly needed here
sys.setrecursionlimit(2000)

def solve():
    # Use fast I/O
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
        
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
    except StopIteration:
        return

    # We need to sort the indices 0 to N-1 based on the resulting sequence S_i
    # S_i is A with A[i] duplicated.
    # Comparison logic:
    # Comp(S_i, S_j) with i < j depends on the first difference.
    # The first diff is at index i+1 (in the new sequence S_i, relative to S_j which hasn't split yet at i).
    # S_i has A[i] at i+1. S_j has A[i+1] at i+1.
    # If A[i] < A[i+1]: S_i < S_j for all j > i. -> "Small" group
    # If A[i] > A[i+1]: S_i > S_j for all j > i. -> "Large" group
    # If A[i] == A[i+1]: S_i == S_{i+1}. Treating blocks of identical values.
    
    small_indices = []
    large_indices = []
    neutral_indices = [] # Indices that are effectively the suffix/end
    
    i = 0
    while i < N:
        # Find block of identical values
        j = i + 1
        while j < N and A[j] == A[i]:
            j += 1
            
        # The block is indices from i to j-1
        current_block = list(range(i, j))
        
        if j < N:
            if A[i] < A[j]:
                # This block is "smaller" than the suffix starting at j
                small_indices.extend(current_block)
            else:
                # This block is "larger" than the suffix starting at j
                large_indices.extend(current_block)
        else:
            # End of array, no right neighbor to compare with
            neutral_indices.extend(current_block)
            
        i = j

    # The sorted order of indices is:
    # 1. Small indices (preserving original relative order)
    # 2. Neutral indices
    # 3. Large indices (reversed original relative order)
    #    Why reversed? Because if i < j and both are Large, S_i > S_j.
    #    So larger S_i comes later in the sorted list.
    
    # Construct the K-th index (0-based list, so K-1)
    # Optimization: We don't need to build the full array if we just want the K-th element
    
    len_small = len(small_indices)
    len_neutral = len(neutral_indices)
    
    target_idx = -1
    
    if K <= len_small:
        target_idx = small_indices[K-1]
    elif K <= len_small + len_neutral:
        target_idx = neutral_indices[K - 1 - len_small]
    else:
        # It's in the large group
        # The large group in sorted order is reversed(large_indices)
        remaining_k = K - len_small - len_neutral
        # item at index `remaining_k - 1` in `reversed(large_indices)`
        # is item at `len - 1 - (remaining_k - 1)` in `large_indices`
        target_idx = large_indices[len(large_indices) - remaining_k]

    # Construct and print the result
    # We need to print A with A[target_idx] doubled
    
    # Using sys.stdout.write for faster output with large N
    output = []
    for idx in range(target_idx + 1):
        output.append(str(A[idx]))
    output.append(str(A[target_idx])) # The clone
    for idx in range(target_idx + 1, N):
        output.append(str(A[idx]))
        
    sys.stdout.write(" ".join(output) + "\n")

if __name__ == '__main__':
    solve()
