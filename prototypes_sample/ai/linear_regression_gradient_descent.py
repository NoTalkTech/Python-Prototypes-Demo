"""
Linear Regression, Gradient Descent(GD)
1. Batch Gradient Descent, BGD
2. Stochastic(随机) Gradient Descent, SGD
3. Mini-batch Gradient Descent, MBGD
"""

import numpy as np
import matplotlib.pyplot as plt


def compute_mse(theta, X_b, y):
    """
    compute_mse 均方误差损失函数

    Args:
        theta (_type_): _description_
        X_b (_type_): _description_
        y (_type_): _description_

    Returns:
        _type_: _description_
    """
    m = len(y)
    return (1 / (2 * m)) * np.sum((X_b.dot(theta) - y) ** 2)


def gradient_descent(X_b, y, learning_rate=0.1, n_iterations=1000):
    """
    gradient_descent 梯度下降算法

    Args:
        X_b (_type_): _description_
        y (_type_): _description_
        learning_rate (float, optional): _description_. Defaults to 0.1.
        n_iterations (int, optional): _description_. Defaults to 1000.

    Returns:
        _type_: _description_
    """
    m = len(y)
    theta = np.random.randn(2, 1)  # 初始化参数 theta
    theta_history = []  # 用于记录每次迭代的 theta
    loss_history = []   # 用于记录每次迭代的损失值

    for iteration in range(n_iterations):
        gradients = (1 / m) * X_b.T.dot(X_b.dot(theta) - y)  # 计算梯度
        theta = theta - learning_rate * gradients  # 更新参数
        theta_history.append(theta.copy())  # 记录参数历史
        loss_history.append(compute_mse(theta, X_b, y))  # 记录损失值

    return theta, loss_history, theta_history


if __name__ == 'main':
    # 生成简单的线性数据
    np.random.seed(42)
    X = 2 * np.random.rand(100, 1)  # 100个样本，单个特征
    y = 4 + 3 * X + np.random.randn(100, 1)  # 假设线性关系 y = 4 + 3X + 噪声

    # 为X添加一列1（偏置项），形成X_b
    X_b = np.c_[np.ones((100, 1)), X]  # 添加x0 = 1到每个实例

    # 设置学习率和迭代次数
    learning_rate = 0.1
    n_iterations = 100

    # 运行梯度下降
    theta_final, loss_history, theta_history = gradient_descent(
        X_b, y, learning_rate, n_iterations)

    # 绘制损失函数值随迭代次数的变化
    plt.plot(loss_history)
    plt.title("Loss Function Over Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("MSE Loss")
    plt.show()

    # 提取 theta0 和 theta1 的历史变化
    theta_0_history = [theta[0][0] for theta in theta_history]
    theta_1_history = [theta[1][0] for theta in theta_history]
    plt.axvline(x=theta_final[0], color='green', linestyle='--', label='Final theta0')
    plt.axhline(y=theta_final[1], color='blue', linestyle='--', label='Final theta1')
    # 绘制参数更新轨迹
    plt.plot(theta_0_history, theta_1_history,
             'b-o', label='Gradient Descent Path')
    plt.title("Theta0 vs Theta1 Update Path")
    plt.xlabel("Theta0")
    plt.ylabel("Theta1")
    plt.legend()
    plt.show()
