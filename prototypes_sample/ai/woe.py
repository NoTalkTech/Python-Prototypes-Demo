# Re-import necessary libraries due to reset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Example data
data = {
    'Income': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    'Default': [0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]
}

# Create DataFrame
df = pd.DataFrame(data)

# Bin income into 4 intervals
df['Income_bin'] = pd.cut(df['Income'], bins=[0, 25, 50, 75, 100], labels=['0-25', '25-50', '50-75', '75-100'])

# Calculate number of good (Default=0) and bad (Default=1) customers in each bin
grouped = df.groupby('Income_bin')['Default'].agg(['count', 'sum'])
grouped.columns = ['Total', 'Bad']

# Calculate number of good customers
grouped['Good'] = grouped['Total'] - grouped['Bad']

# Total number of good and bad customers
total_good = df['Default'].value_counts()[0]
total_bad = df['Default'].value_counts()[1]

grouped['Bad_dist'] = grouped['Bad'] / total_bad
grouped['Good_dist'] = grouped['Good'] / total_good

# 重新计算 WOE 值，基于 Bad distribution / Good distribution
grouped['WOE'] = np.log(grouped['Bad_dist'] / grouped['Good_dist'])

# 打印 WOE 结果
print(grouped[['Good', 'Bad', 'Good_dist', 'Bad_dist', 'WOE']])

# 绘制 WOE 值的图表并添加 y = 0 的虚线
plt.figure(figsize=(8, 6))
bars = plt.bar(grouped.index, grouped['WOE'], color='lightblue')

# 添加 y = 0 的虚线
plt.axhline(0, color='gray', linestyle='--', label='woe = 0')

# 为每个柱状图添加对应数值
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

plt.title('WOE Values by Income Bin')
plt.xlabel('Income Bin')
plt.ylabel('Weight of Evidence (WOE)')
plt.legend()
plt.show()