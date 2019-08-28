# -*- coding: UTF-8 -*-
"""
Description: SMS Spam Detection
Author: Wallace Huang
Date: 2019/7/22
Version: 1.0
"""
import os
import re
import string
from collections import Counter

import nltk
import pandas as pd
from nltk.corpus import stopwords
from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attr):
        self.attr_names = attr

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.rename(columns={"v1": "Type", "v2": "Text"})
        return X[self.attr_names]


class AddExtraAttr(BaseEstimator, TransformerMixin):
    def __init__(self, attr):
        self.attr_name = attr

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.values
        X = pd.DataFrame(X, columns=[self.attr_name])
        X['Length'] = X[self.attr_name].apply(len)
        #         findCapitalCount = lambda x: sum(map(str.isupper, x[self.attr_name].split()))
        #         X["CapitalCount"] = X.apply(findCapitalCount, axis=1)
        #         findWordCount = lambda x: len(x[self.attr_name].split())
        #         X["WordCount"] = X.apply(findWordCount, axis=1)
        #         X["CapitalRate"] = X["CapitalCount"] / X["WordCount"]
        return X[["Length"]]


class FindCount(BaseEstimator, TransformerMixin):
    def __init__(self, attr):
        self.attr_name = attr

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        Y = []
        for index, row in X.iterrows():
            row[self.attr_name] = re.sub(r'\d+(?:\.\d*(?:[eE]\d+))?', 'NUMBER', row[self.attr_name])
            no_punc = [ch for ch in row[self.attr_name] if ch not in string.punctuation]
            punc = [(" " + ch + " ") for ch in row[self.attr_name] if ch in string.punctuation]
            word_list = "".join(no_punc + punc).split()
            useful_words = [word.lower() for word in word_list if word.lower() not in stopwords.words("english")]
            word_counts = Counter(useful_words)
            stemmed_word_counts = Counter()
            for word, count in word_counts.items():
                stemmed_word = stemmer.stem(word)
                stemmed_word_counts[stemmed_word] += count
            word_counts = stemmed_word_counts
            Y.append(word_counts)
        return Y


class ConvertToVector(BaseEstimator, TransformerMixin):
    def __init__(self, vocabulary_size=1000):
        self.vocabulary_size = vocabulary_size

    def fit(self, X, y=None):
        total_count = Counter()
        for word_count in X:
            for word, count in word_count.items():
                total_count[word] += count
        most_common = total_count.most_common()[:self.vocabulary_size]
        self.most_common_ = most_common
        self.vocabulary_ = {word: index + 1 for index, (word, count) in enumerate(most_common)}
        return self

    def transform(self, X, y=None):
        rows = []
        cols = []
        data = []
        for row, word_count in enumerate(X):
            for word, count in word_count.items():
                rows.append(row)
                cols.append(self.vocabulary_.get(word, 0))
                data.append(count)
        return csr_matrix((data, (rows, cols)), shape=(len(X), self.vocabulary_size + 1))


if __name__ == '__main__':
    sample_file = '../resources/spam.csv'
    if not os.access(sample_file, os.F_OK):
        print('FileNotFoundError: %s not found.' % sample_file)
        exit(-1)
    else:
        data = pd.read_csv(sample_file, encoding='latin-1', low_memory=True)
        print(data.head(1))
        # print(data.info)
        unimportant_col = ["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"]
        data.drop(unimportant_col, axis=1, inplace=True)
        print(data.head(1))
        data.rename(columns={"v1": "Type", "v2": "Text"}, inplace=True)
        print(data.head(1))
        train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
        train_data.info()
        test_data.info()
        print(train_data.describe())
        print(train_data.groupby("Type").describe())
        # train_data.Type.value_counts().plot.pie(autopct='%0.2f%%', shadow=True)
        # plt.show()

        train_data['Length'] = train_data['Text'].apply(len)
        print(train_data.head(5))

        # train_data.hist(column='Length', by='Type', bins=60, figsize=(12, 4))
        # plt.show()
        findCapitalCount = lambda x: sum(map(str.isupper, x['Text'].split()))
        train_data["CapitalCount"] = train_data.apply(findCapitalCount, axis=1)
        print(train_data.head(5))

        # train_data.hist(column='CapitalCount', by='Type', bins=30, figsize=(12, 4))
        # plt.show()
        findWordCount = lambda x: len(x['Text'].split())
        train_data["WordCount"] = train_data.apply(findWordCount, axis=1)
        print(train_data.head(5))

        train_data["CapitalRate"] = train_data["CapitalCount"] / train_data["WordCount"]
        print(train_data.head(5))

        # train_data.hist(column='CapitalRate',by='Type',bins=30,figsize=(12,4))
        # plt.show()

        stopwords.words("english")

        stemmer = nltk.PorterStemmer()
        for word in ("Computations", "Computation", "Computing", "Computed", "Compute", "Compulsive"):
            print(word, "=>", stemmer.stem(word))
        cat_attr = ["Text"]

        main_pipeline = Pipeline([
            ('selector', DataFrameSelector(cat_attr)),
            ('find_count', FindCount(cat_attr[0])),
            ('convert_to_vector', ConvertToVector()),
        ])

        extra_pipeline = Pipeline([
            ('selector', DataFrameSelector(cat_attr)),
            ('add_extra', AddExtraAttr(cat_attr[0])),
        ])

        full_pipeline = FeatureUnion(transformer_list=[
            ('main_pipeline', main_pipeline),
            ('extra_pipeline', extra_pipeline),
        ])

        train_prepared = full_pipeline.fit_transform(train_data)

        y_train = train_data["Type"]
        encoder = LabelEncoder()
        type_encoded = encoder.fit_transform(y_train)

        # Logistic Regression
        log_clf = LogisticRegression(solver="liblinear", random_state=42)
        score = cross_val_score(log_clf, train_prepared, type_encoded, cv=3, verbose=3)
        score.mean()

        # SGD
        sgd_clf = SGDClassifier(random_state=42)
        score = cross_val_score(sgd_clf, train_prepared, type_encoded, cv=3, verbose=3)
        score.mean()

        # MultinomialNB
        mnb_clf = MultinomialNB()
        score = cross_val_score(mnb_clf, train_prepared, type_encoded, cv=3, verbose=3)
        score.mean()

        # BernoulliNB
        bnb_clf = BernoulliNB()
        score = cross_val_score(bnb_clf, train_prepared, type_encoded, cv=3, verbose=3)
        score.mean()

        from sklearn.metrics import precision_score, recall_score

        y_test = test_data["Type"]
        encoder = LabelEncoder()
        type_encoded = encoder.fit_transform(y_test)

        X_test_transformed = full_pipeline.transform(test_data)

        bnb_clf = BernoulliNB()
        bnb_clf.fit(train_prepared, y_train)

        y_pred = bnb_clf.predict(X_test_transformed)
        encoder = LabelEncoder()
        y_pred = encoder.fit_transform(y_pred)

        print("Precision BernoulliNB: {:.2f}%".format(100 * precision_score(type_encoded, y_pred)))
        print("Recall BernoulliNB: {:.2f}%\n".format(100 * recall_score(type_encoded, y_pred)))

        mnb_clf = MultinomialNB()
        mnb_clf.fit(train_prepared, y_train)

        y_pred = mnb_clf.predict(X_test_transformed)
        encoder = LabelEncoder()
        y_pred = encoder.fit_transform(y_pred)

        print("Precision MultinomialNB: {:.2f}%".format(100 * precision_score(type_encoded, y_pred)))
        print("Recall MultinomialNB: {:.2f}%\n".format(100 * recall_score(type_encoded, y_pred)))

        sgd_clf = SGDClassifier(random_state=42)
        sgd_clf.fit(train_prepared, y_train)

        y_pred = sgd_clf.predict(X_test_transformed)
        encoder = LabelEncoder()
        y_pred = encoder.fit_transform(y_pred)

        print("Precision SGD: {:.2f}%".format(100 * precision_score(type_encoded, y_pred)))
        print("Recall SGD: {:.2f}%\n".format(100 * recall_score(type_encoded, y_pred)))

        log_clf = LogisticRegression(solver="liblinear", random_state=42)
        log_clf.fit(train_prepared, y_train)

        y_pred = log_clf.predict(X_test_transformed)
        encoder = LabelEncoder()
        y_pred = encoder.fit_transform(y_pred)

        print("Precision Logistic Regression: {:.2f}%".format(100 * precision_score(type_encoded, y_pred)))
        print("Recall Logistic Regression: {:.2f}%".format(100 * recall_score(type_encoded, y_pred)))
