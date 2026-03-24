import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

def main():
    # 1. 加载数据
    # 尝试加载 iris.csv, iris.txt 或 iris.data
    file_path = None
    data = None
    
    # 尝试列表
    files_to_try = [
        ('iris.csv', ','),
        ('iris.txt', ' '),
        ('iris.data', ',')
    ]

    for fname, sep in files_to_try:
        try:
            # 尝试读取
            # iris.txt 看起来是空格分隔，且带引号
            if fname == 'iris.txt':
                 data = pd.read_csv(fname, sep=r'\s+', index_col=0)
            else:
                 data = pd.read_csv(fname, index_col=0)
            
            print(f"成功加载文件: {fname}")
            file_path = fname
            break
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"尝试加载 {fname} 时出错: {e}")
            continue

    if data is None:
        print("错误: 未找到 iris.csv, iris.txt 或 iris.data 文件")
        return

    print("数据预览:")
    print(data.head())
    print("-" * 30)

    # 2. 数据预处理
    # 提取特征和标签
    # 特征列: Sepal.Length, Sepal.Width, Petal.Length, Petal.Width
    X = data[['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width']]
    # 标签列: Species
    y = data['Species']

    # 划分训练集和测试集 (80% 训练, 20% 测试)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 数据标准化 (SVM 对特征缩放比较敏感，建议进行标准化)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 3. 创建 SVM 分类器
    # 使用径向基函数 (RBF) 核，这是常用的默认核函数
    clf = svm.SVC(kernel='rbf', C=1.0, gamma='scale')

    # 4. 训练模型
    print("开始训练 SVM 模型...")
    clf.fit(X_train, y_train)
    print("训练完成。")
    print("-" * 30)

    # 5. 模型评估
    # 在测试集上进行预测
    y_pred = clf.predict(X_test)

    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)
    print(f"模型准确率: {accuracy:.2f}")
    print("-" * 30)

    # 输出详细的分类报告
    print("分类报告:")
    print(classification_report(y_test, y_pred))

    # 简单的预测演示
    print("-" * 30)
    print("新样本预测演示:")
    # 构造两个新样本 (需要先标准化)
    new_samples = [[5.1, 3.5, 1.4, 0.2], [6.5, 3.0, 5.2, 2.0]]
    
    # 为了避免警告，将新样本转换为 DataFrame，并指定列名
    new_samples_df = pd.DataFrame(new_samples, columns=['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width'])
    
    new_samples_scaled = scaler.transform(new_samples_df)
    predictions = clf.predict(new_samples_scaled)
    
    for sample, pred in zip(new_samples, predictions):
        print(f"特征: {sample} -> 预测类别: {pred}")

if __name__ == "__main__":
    main()
    print("202378040607李世奇")
