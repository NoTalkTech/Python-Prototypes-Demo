# -*- coding: UTF-8 -*-
"""
Description: Train simple Xgboost model
Author: Wallace Huang
Date: 2019/9/20
Version: 1.0
"""
import lightgbm as lgb
import numpy as np
import os
import xgboost as xgb

if __name__ == '__main__':
    pwd = os.getcwd()
    print('>>> pwd: {}'.format(pwd))

    train_data = np.random.rand(50000, 10)  # 50000 entities, each contains 10 features
    train_label = np.random.randint(2, size=50000)  # binary target
    d_train = xgb.DMatrix(train_data, label=train_label)
    eval_data = np.random.rand(10000, 10)  # 10000 entities, each contains 10 features
    eval_label = np.random.randint(2, size=10000)  # binary target
    d_eval = xgb.DMatrix(train_data, label=train_label)

    # Train xgboost model
    param = {'max_depth': 2, 'eta': 1, 'objective': 'binary:logistic', 'nthread': 4, 'eval_metric': 'auc'}
    evallist = [(d_eval, 'eval'), (d_train, 'train')]
    num_round = 100
    bst_xgb = xgb.train(param, d_train, num_round, evallist)
    bst_xgb.save_model('{}/bst_xgb_0001.model'.format(pwd))

    # Train lightGBM model
    train_set = lgb.Dataset(train_data, label=train_label)
    valid_set = lgb.Dataset(eval_data, label=eval_label)
    param = {'num_leaves': 31, 'objective': 'binary', 'metric': 'auc'}
    num_round = 100
    bst_lgb = lgb.train(param, train_set, num_round, valid_sets=[valid_set])
    bst_lgb.save_model('{}/bst_lgb_0001.model'.format(pwd))


def train(dtrain, deval, params, num_rounds, m_type):
    if m_type == 'xgb':
        eval_list = [(deval, 'eval'), (dtrain, 'train')]
        bst = xgb.train(params, dtrain, num_rounds, eval_list)
        return bst
    elif m_type == 'lgb':
        bst = lgb.train(params, dtrain, num_rounds, valid_sets=[deval])
        return bst
    else:
        raise ValueError('un-supported model type: {}'.format(m_type))
