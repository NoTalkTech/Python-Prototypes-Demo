import sys
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from statsmodels.stats.proportion import proportions_ztest


logging.basicConfig(stream=sys.stdout,
                    format='[%(asctime)s]{%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    level=logging.INFO)


def stardard_scaler(data):
    """
    stardard_scaler
    Args:
        data (_type_): data to be standardized
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(pd.DataFrame(data))
    logging.info("raw data: {}".format(data))
    logging.info("scaled data: {}".format(scaled_data))
    return scaled_data


def caclucate_woe(data: pd.DataFrame, bins: list):
    data['bin'] = pd.cut(data['X'], bins=bins)
    grouped = data.groupby('bin')['y'].agg(['count', 'sum'])
    grouped.columns = ['total', 'good']  # 'good' means y=1
    grouped['bad'] = grouped['total'] - grouped['good']  # 'bad' means y=0
    grouped['woe'] = np.log(
        (grouped['good'] / grouped['good'].sum()) / (grouped['bad'] / grouped['bad'].sum()))
    return grouped


def estimate_parameters_summary(data):
    # Step 1: 添加截距项
    data['intercept'] = 1

    # Step 2: 定义特征矩阵 X 和目标变量 y
    X = data[['intercept', 'X']]
    y = data['y']

    # Step 3: 使用 statsmodels 进行逻辑回归
    model = sm.Logit(y, X).fit()

    # Step 4: 输出模型的详细参数
    print(model.summary2())

    # 获取具体参数值
    params = model.params
    std_errors = model.bse
    wald_chi2 = (params / std_errors) ** 2
    p_values = model.pvalues

    # 将参数汇总到一个表格中
    summary_df = pd.DataFrame({
        'Estimate': params,
        'Std. Error': std_errors,
        'Wald Chi-Square': wald_chi2,
        'Pr > Chi Sq': p_values
    })
    return summary_df


def z_test(conversions, nobs):
    stat, p_value = proportions_ztest(conversions, nobs)
    logging.info(f"Z 值: {stat}, p 值: {p_value}")


if __name__ == 'main':
    mock_data = {
        'Feature1': [2, 4, 6, 8, 10],
        'Feature2': [1, 3, 5, 7, 9],
        'Feature3': [2, 4, 6, 8, 10]
    }
    stardard_scaler(mock_data)
    data = pd.DataFrame({
        'X': [0, 1.2, 2.3, 3.4, 4.3, 5.2, 4.3, 4.9],
        'y': [0, 1, 0, 1, 0, 1, 0, 1]
    })
    caclucate_woe(data, [0, 2, 4, 6])

    data2 = pd.DataFrame({
        'X': [0, 1.2, 2.3, 3.4, 4.3, 5.2, 4.3, 4.9, 4.3, 4.1, 4.03, 4.32,
              3.6, 3.7, 4.01, 5.1, 4.5, 4.9, 4.6, 5.12, 6.34, 5.1, 4.3,
              3.6, 3.7, 4.01, 5.1, 4.5, 4.9, 4.6, 5.12, 6.34, 5.1, 4.3],
        'y': [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    })
    data2['X'] = stardard_scaler(data2['X'])
    estimate_parameters_summary(data2)

    conversions = np.array([420, 100])
    nobs = np.array([3000, 1000])
    stat, p_value = proportions_ztest(conversions, nobs)
    print(f"Z 值: {stat}, p 值: {p_value}")
