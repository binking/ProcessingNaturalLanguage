# -*-coding:utf8-*-
# /usr/bin/python3
import re
import jieba
import string
import pymongo
import numpy as np
from datetime import datetime as dt
from collections import OrderedDict
from EditDistance import LevenshteinMethod

text_1 = u"妈妈说，我们不能在墙上画画"
text_2 = u"子曰，咱不可以在建筑物上乱涂乱画"

THRESHOLD = 0.3
short_text_1 = u'计算机价格'
short_text_2 = u'电脑费用'
client = pymongo.MongoClient('123.206.65.125', 27017)
wv_coll = client.sogou_corpus.sogou_pedia_corpus
# print(client.database_names())


def format_word_vector(text):
    print("Pre processing string", text)
    tokens = jieba.cut(text, cut_all=False)
    word_vector = OrderedDict()
    for t in tokens:
        if t in string.punctuation + '+——！，。？、~@#￥%……&*（）':
            continue
        if t not in word_vector:
            wv = wv_coll.find_one({'word': t})
            if wv:  # if not existed, None
                word_vector[t] = np.array(wv['vector'])
    return word_vector


def tokenize(text):
    no_punc = []
    tokens = jieba.cut(text, cut_all=False)
    for t in tokens:
        if t in string.punctuation + '+——！，。？、~@#￥%……&*（）':
            continue
        if t not in no_punc:
            no_punc.append(t)
    return no_punc


def binary_threshold(distance):
    print(distance)
    if distance > THRESHOLD:
        return 1
    else:
        return 0


def compute_cosine_distance(vec1, vec2):
    dist = np.dot(vec1, vec2) / (sum(vec1*vec1) + sum(vec2*vec2))
    return dist


def compute_semantic_similarity(x, y):
    matrix = []
    wv_x = format_word_vector(x)
    wv_y = format_word_vector(y)
    for i in range(len(wv_x)+1):
        matrix.append([0] * (len(wv_y)+1)) # initialize the matrix with zeros
    for i in range(len(wv_x)+1):
        matrix[i][0] = i # Fill in the first column with ascending integers
    for j in range(len(wv_y) + 1):
        matrix[0][j] = j # Fill in the first row with ascending integers
    for i, i_key in enumerate(wv_x):
        for j, j_key in enumerate(wv_y):
            # Fill in other elements
            # import pdb; pdb.set_trace()
            dist = compute_cosine_distance(wv_x[i_key], wv_y[j_key])
            print("Binary value between %s and %s: " % (i_key, j_key), end=' ')
            sim = binary_threshold(dist)
            delta = 1 if sim == 1 else 0
            distDiag = matrix[i][j] + delta
            distVer = matrix[i][j+1] + 1
            distHor = matrix[i+1][j] + 1
            matrix[i+1][j+1] = min(distDiag, distHor, distVer)
    # print(matrix)
    return matrix[-1][-1]


def compute_edit_distance(x, y):
    tokens1 = tokenize(x)
    tokens2 = tokenize(y)
    return LevenshteinMethod(tokens1, tokens2)

if __name__ == '__main__':
    start = dt.now()
    print("Normal Edit Distance: ", compute_edit_distance(short_text_1, short_text_2))
    print("Semantic Edit Distance: ", compute_semantic_similarity(short_text_1, short_text_2))
    print("Normal Edit Distance: ", compute_edit_distance(text_1, text_2))
    print("Semantic Edit Distance: ", compute_semantic_similarity(text_1, text_2))
    client.close()
    print("It takes %s to run .." % (dt.now() - start))
