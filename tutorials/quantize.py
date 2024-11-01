import numpy as np
import matplotlib.pyplot as plt

# 生成模拟长尾分布数据
np.random.seed(0)
data = -np.random.exponential(scale=1.0, size=1000) + 2  # 生成负值长尾分布，并平移使最大值为正数
data = np.clip(data, -2, 5)  # 限制数据范围 [-2, 5]

# 定义密集和稀疏区域的步长
# 根据数据分布计算密集和稀疏区域的步长
hist, bins = np.histogram(data, bins=50)
max_density = np.max(hist)
min_density = np.max(hist[hist > 0])  # 最小非零密度

# 根据密度比例动态调整步长
density_ratio = max_density / min_density
scale_dense = 0.05 * np.sqrt(density_ratio)  # 密集区域使用更小的步长
scale_sparse = 0.5 * np.sqrt(density_ratio)  # 稀疏区域使用更大的步长

# 定义量化函数
def quantize(x, scale_dense, scale_sparse):
    if -1.0 <= x <= 1.0:
        # 密集区间量化
        x_int = round(x / scale_dense)
        x_dequant = x_int * scale_dense
    else:
        # 稀疏区间量化
        x_int = round(x / scale_sparse)
        x_dequant = x_int * scale_sparse
    return x_int, x_dequant

def main():
    # 对数据进行量化与反量化
    quantized_values = [quantize(x, scale_dense, scale_sparse) for x in data]
    quantized_ints, dequantized_values = zip(*quantized_values)

    # 可视化量化前后数据的分布
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.hist(data, bins=50, color="skyblue", edgecolor="black", alpha=0.7)
    plt.title("Original Data Distribution")
    plt.xlabel("Value")
    plt.ylabel("Frequency")

    plt.subplot(1, 2, 2)
    plt.hist(dequantized_values, bins=50, color="salmon", edgecolor="black", alpha=0.7)
    plt.title("Dequantized Data Distribution")
    plt.xlabel("Value")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

    # 打印部分原始数据、量化值和反量化结果
    print("原始值\t量化整数值\t反量化值")
    for i in range(10):
        print(f"{data[i]:.2f}\t{quantized_ints[i]}\t{dequantized_values[i]:.2f}")

if __name__ == "__main__":
    main()
