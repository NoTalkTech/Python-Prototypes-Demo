#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
Description: linear_regression_model, predict boston house price
Author: Wallace Huang
Date: 2020/07/07
Version: 1.0
"""
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import learning_curve
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn import datasets
import matplotlib.pyplot as plt
import time
import numpy as np
from sklearn.metrics import r2_score


def polynomial_model(degree=1):
    polynomial_features = PolynomialFeatures(degree=degree, include_bias=False)
    linear_regression = LinearRegression(normalize=True)  # 归一化数据进行训练，可加快算法收敛速度
    pipeline = Pipeline([("polynomial_feature", polynomial_features),
                        ("linear_regression", linear_regression)])
    return pipeline


#定义学习曲线函数
def plot_learning_curve(plt, estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : 训练集的特征
        array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : 训练集的标签
        array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : 交叉验证结果
        int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.title(title)  # 画出标题
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")  # 横轴标签
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)  # 均值
    train_scores_std = np.std(train_scores, axis=1)  # 方差
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")  # 红色区域是准确性平均值的方差空间
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o--', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt


def linear_regression_model():
    loaded_data = datasets.load_boston()
    data_X = loaded_data.data
    data_y = loaded_data.target
    X_train, X_test, Y_train, Y_test = train_test_split(
        data_X, data_y, test_size=0.1, random_state=3)

    #定义多项式模型函数
    model = polynomial_model(degree=1)  # 使用一阶多项式模型拟合
    start = time.perf_counter()
    model.fit(X_train,Y_train)
    #模型预测与评估
    train_score = model.score(X_train, Y_train)
    cv_score = model.score(X_test, Y_test)

    print('使用一阶多项式拟合结果')
    l_model=model.get_params()['linear_regression']
    print('w=',l_model.coef_)  # 输出权重矩阵
    print('b=',l_model.intercept_)  # 输出偏移量
    print('elaspe:{0:.6f};train_score:{1:0.6f};cv_score:{2:.6f}'.format(
        time.perf_counter()-start, train_score, cv_score))

    
    #定义多项式模型函数
    model = polynomial_model(degree=2)  # 使用二阶多项式模型拟合
    start = time.perf_counter()
    model.fit(X_train, Y_train)

    #模型预测与评估
    train_score = model.score(X_train, Y_train)
    cv_score = model.score(X_test, Y_test)

    print('使用二阶多项式拟合结果')
    l_model=model.get_params()['linear_regression']
    print('w=',l_model.coef_)  # 输出权重矩阵
    print('b=',l_model.intercept_)  # 输出偏移量
    print('elaspe:{0:.6f};train_score:{1:0.6f};cv_score:{2:.6f}'.format(
        time.perf_counter()-start, train_score, cv_score))

    model = polynomial_model(degree=3)  # 使用三阶多项式模型拟合
    start = time.perf_counter()
    model.fit(X_train, Y_train)

    #模型预测与评估
    train_score = model.score(X_train, Y_train)
    cv_score = model.score(X_test, Y_test)
    print('使用三阶多项式拟合结果')
    l_model = model.get_params()['linear_regression']
    print('w=', l_model.coef_)  # 输出权重矩阵
    print('b=', l_model.intercept_)  # 输出偏移量
    print('elaspe:{0:.6f};train_score:{1:0.6f};cv_score:{2:.6f}'.format(
        time.perf_counter()-start, train_score, cv_score))

    #画出学习曲线
    cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
    plt.figure(figsize=(18, 4), dpi=200)
    title = 'Learning Curves (degree={0})'
    degrees = [1, 2, 3]

    start = time.perf_counter()
    plt.figure(figsize=(18, 4), dpi=200)
    for i in range(len(degrees)):
        plt.subplot(1, 3, i+1)
        plot_learning_curve(plt, polynomial_model(degrees[i]), title.format(
            degrees[i]), data_X, data_y, ylim=(0.01, 1.01), cv=cv)
        print('=> elaspe:{0:.6f}'.format(time.perf_counter()-start))
    
    model = LinearRegression()
    model.fit(X_train, Y_train)
    print('w=',model.coef_)  # 输出权重矩阵
    print('b=',model.intercept_)  # 输出偏移量
    print('cv_score=',model.score(X_test, Y_test))  # 输出准确度
    
    
if __name__ == "__main__":
    linear_regression_model()
