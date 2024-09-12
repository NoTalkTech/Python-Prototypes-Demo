import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification


def sigmoid(z):
    """
    sigmoid Sigmoid函数

    Args:
        z (_type_): _description_

    Returns:
        _type_: _description_
    """
    return 1 / (1 + np.exp(-z))


def compute_cost(theta, X_b, y):
    """
    compute_cost 损失函数

    Args:
        theta (_type_): _description_
        X_b (_type_): _description_
        y (_type_): _description_

    Returns:
        _type_: _description_
    """
    m = len(y)
    h = sigmoid(X_b.dot(theta))
    epsilon = 1e-5  # 防止log(0)
    return - (1 / m) * np.sum(y * np.log(h + epsilon) + (1 - y) * np.log(1 - h + epsilon))


def gradient_descent(X_b, y, learning_rate=0.1, n_iterations=1000):
    """
    gradient_descent 梯度下降

    Args:
        X_b (_type_): _description_
        y (_type_): _description_
        learning_rate (float, optional): _description_. Defaults to 0.1.
        n_iterations (int, optional): _description_. Defaults to 1000.

    Returns:
        _type_: _description_
    """
    m = len(y)
    theta = np.random.randn(X_b.shape[1], 1)  # 初始化参数 theta
    theta_history = []  # 记录每次迭代的 theta 值
    cost_history = []   # 记录每次迭代的损失值

    for iteration in range(n_iterations):
        h = sigmoid(X_b.dot(theta))  # 计算预测值
        gradients = (1 / m) * X_b.T.dot(h - y)  # 计算梯度
        theta = theta - learning_rate * gradients  # 更新参数

        # 记录 theta 和损失值
        theta_history.append(theta.copy())
        cost_history.append(compute_cost(theta, X_b, y))

    return theta, cost_history, theta_history


if __name__ == 'main':
    # 生成二分类数据集
    X, y = make_classification(n_samples=100, n_features=1, n_informative=1, n_redundant=0,
                               n_clusters_per_class=1, random_state=42)
    y = y.reshape(-1, 1)  # 将标签转为列向量
    # 为X添加偏置项
    X_b = np.c_[np.ones((X.shape[0], 1)), X]  # 添加偏置项

    # 设置学习率和迭代次数
    learning_rate = 0.1
    n_iterations = 1000

    # 运行梯度下降
    theta_final, cost_history, theta_history = gradient_descent(
        X_b, y, learning_rate, n_iterations)

    # 绘制损失函数变化
    plt.plot(cost_history)
    plt.title("Cost Function Over Iterations (Logistic Regression)")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.show()

    # 绘制分类边界
    x_values = [np.min(X), np.max(X)]
    y_values = -(theta_final[0] + np.dot(theta_final[1], x_values))
    # 添加虚线标记最终的 theta 值
    plt.axvline(x=theta_final[0], color='green', linestyle='--', label='Final theta0')
    plt.axhline(y=theta_final[1], color='blue', linestyle='--', label='Final theta1')
    plt.scatter(X, y, label="Data points")
    plt.plot(x_values, y_values, label="Decision Boundary", color='red')
    plt.title("Logistic Regression Decision Boundary")
    plt.xlabel("Feature")
    plt.ylabel("Probability")
    plt.legend()
    plt.show()
