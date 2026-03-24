"""
用纯 Python 实现的二分类感知器（Perceptron），并用它学习逻辑 AND 和 OR。
- 不依赖第三方库（如 numpy），便于在任意环境直接运行。
- 包含训练、预测与简单演示。
"""
from __future__ import annotations
from typing import Iterable, List, Sequence, Tuple


class Perceptron:
    """一个简单的感知器实现（含偏置项）。

    参数:
        lr: 学习率
        epochs: 最大训练轮数
        verbose: 是否打印每轮训练的错误数和权重
    """

    def __init__(self, lr: float = 0.1, epochs: int = 20, verbose: bool = False) -> None:
        self.lr = float(lr)
        self.epochs = int(epochs)
        self.verbose = bool(verbose)
        self._w: List[float] | None = None  # [w1, w2, ..., wbias]

    @property
    def weights(self) -> List[float]:
        if self._w is None:
            raise RuntimeError("模型尚未训练，权重不可用")
        return self._w

    def _init_weights(self, n_features: int) -> None:
        # 使用 0 初始化即可收敛到 AND/OR 的解
        self._w = [0.0] * (n_features + 1)  # 最后一位为 bias 权重

    def _net_input(self, x: Sequence[float]) -> float:
        assert self._w is not None, "请先调用 fit 训练模型"
        s = self._w[-1]  # bias * 1
        for i in range(len(x)):
            s += self._w[i] * float(x[i])
        return s

    def predict_one(self, x: Sequence[float]) -> int:
        """对单个样本做 0/1 预测（阶跃函数）。"""
        return 1 if self._net_input(x) >= 0 else 0

    def predict(self, X: Iterable[Sequence[float]]) -> List[int]:
        return [self.predict_one(x) for x in X]

    def fit(self, X: List[Sequence[float]], y: List[int]) -> "Perceptron":
        if not X:
            raise ValueError("X 不能为空")
        if len(X) != len(y):
            raise ValueError("X 和 y 的长度需一致")
        n_features = len(X[0])
        self._init_weights(n_features)

        for epoch in range(self.epochs):
            errors = 0
            for xi, target in zip(X, y):
                pred = self.predict_one(xi)
                update = self.lr * (int(target) - int(pred))
                if update != 0:
                    # 更新权重 w_i <- w_i + lr * (t - y) * x_i
                    for i in range(n_features):
                        self._w[i] += update * float(xi[i])  # type: ignore[index]
                    # 更新偏置 w_b <- w_b + lr * (t - y)
                    self._w[-1] += update  # type: ignore[index]
                    errors += 1
            if self.verbose:
                print(f"epoch={epoch+1:02d} errors={errors} weights={self._w}")
            if errors == 0:
                break
        return self


def logic_dataset(kind: str) -> Tuple[List[List[int]], List[int]]:
    """返回 AND/OR 的数据集 (X, y)。

    X 顺序固定为: [0,0], [0,1], [1,0], [1,1]
    """
    kind_upper = kind.upper()
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    if kind_upper == "AND":
        y = [0, 0, 0, 1]
    elif kind_upper == "OR":
        y = [0, 1, 1, 1]
    else:
        raise ValueError("kind 仅支持 'AND' 或 'OR'")
    return X, y


def demo(kind: str, lr: float = 0.1, epochs: int = 20, verbose: bool = True) -> None:
    X, y = logic_dataset(kind)
    clf = Perceptron(lr=lr, epochs=epochs, verbose=verbose).fit(X, y)
    preds = clf.predict(X)
    print(f"\n[{kind}] 训练完成：")
    print("权重(含 bias):", clf.weights)
    print("输入 X:       ", X)
    print("真实标签 y:    ", y)
    print("预测结果 pred: ", preds)


if __name__ == "__main__":
    # 演示 AND
    print('202378040607李世奇')
    print("\n" + "-" * 60 + "\n")
    demo("AND", lr=0.2, epochs=20, verbose=True)
    print("\n" + "-" * 60 + "\n")
    # 演示 OR决策树（ID3）算法
    demo("OR", lr=0.2, epochs=20, verbose=True)
    
