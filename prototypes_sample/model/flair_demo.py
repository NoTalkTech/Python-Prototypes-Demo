# -*- coding: UTF-8 -*-
"""
Description: Flair Model
Author: Wallace Huang
Date: 2019/7/21
Version: 1.0
"""

import os

from flair.data import Sentence
from flair.models import TextClassifier

if __name__ == '__main__':
    # classifier = TextClassifier.load('en-sentiment')
    classifier = TextClassifier.load(os.getcwd() + '/imdb.pt')
    s_ls = ['Flair is pretty neat!', 'Chaos hated human beings.', 'Mike David did it alone.']
    for s in s_ls:
        sentence = Sentence(s)
        print(sentence)
        # print sentence with predicted labels
        classifier.predict(sentence)
        print('# %s # \nabove is: %s \n' % (s, sentence.labels))
