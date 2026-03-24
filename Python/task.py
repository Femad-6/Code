from typing import List, Dict

def first_order_lag_filter(data: List[List[float]], alpha: float) -> List[List[float]]:
    if not data:
        return []
    num_signals = len(data[0])
    num_samples = len(data)
    filtered = [data[0].copy()]
    for i in range(1, num_samples):
        current_filtered = []
        for j in range(num_signals):
            y = alpha * data[i][j] + (1 - alpha) * filtered[i-1][j]
            current_filtered.append(y)
        filtered.append(current_filtered)
    return filtered


def compare_statistics(original: List[List[float]], filtered: List[List[float]]) -> Dict[str, Dict[str, float]]:
    if not original or not filtered:
        return {}
    
    num_samples = len(original)
    
    # 定义信号名称映射
    signal_names = ['Pitch', 'Roll']
    
    # 计算每个信号的均值差、方差差和范围差
    result = {}
    for j in range(len(signal_names)):
        # 提取原始数据和滤波后数据
        original_data = [row[j] for row in original]
        filtered_data = [row[j] for row in filtered]
        
        # 计算均值
        original_mean = sum(original_data) / num_samples
        filtered_mean = sum(filtered_data) / num_samples
        mean_diff = original_mean - filtered_mean
        
        # 计算方差
        original_var = sum((x - original_mean)**2 for x in original_data) / num_samples
        filtered_var = sum((x - filtered_mean)**2 for x in filtered_data) / num_samples
        var_diff = original_var - filtered_var
        
        # 计算范围
        original_range = max(original_data) - min(original_data)
        filtered_range = max(filtered_data) - min(filtered_data)
        range_diff = original_range - filtered_range
        
        # 存储结果，保留4位小数
        result[signal_names[j]] = {
            'mean_diff': round(mean_diff, 4),
            'var_diff': round(var_diff, 4),
            'range_diff': round(range_diff, 4)
        }
    
    return result


if __name__ == '__main__':

    data = [
        [10.0, 5.0],
        [12.0, 8.0],
        [20.0, 7.0],
        [18.0, 10.0]
    ]
    alpha = 0.5

    filtered = first_order_lag_filter(data, alpha)
    print(filtered)
    result = compare_statistics(data, filtered)
    print(result)
