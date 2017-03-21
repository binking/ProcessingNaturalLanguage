# -*-conding:utf8-*-
# /usr/bin/python3
import re
import jieba
import string
import pymongo
import numpy as np
from datetime import datetime as dt
from collections import OrderedDict
from EditDistance import LevenshteinMethod

text_1 = """在自由城建立后的最初的十年间，所有的毒品在这里都被允许使用和交易。这也造成了极其严重的后果。仅仅在 1978 和 1979 年这两年，就有 10 人因为吸食毒品过量死在了自由城。自由城的居民们再也无法忍受这种毒品泛滥的情况，在尝试与丹麦警察合作失败后，自由城中所有的居民，无论男女老幼，纷纷走上街头，对自由城进行了 40 天的昼夜不断的巡逻，每当遇见毒贩子，就对他们发出最后的通牒：放弃毒品或者离开自由城。最终，毒贩子们被武力驱赶出了自由城，也有超过 60 名瘾君子被送进了戒毒所。这是 Christiania 历史上著名的“Junk Blockade”事件。至此，自由城开始禁止一切“hard drug”的使用与交易。 “Junk Blockade”期间，自由城居民们在城中竖起了“Junk is death”的牌子 虽然 hard drug 被驱赶出了自由城。但是 40 多年来，以大麻为代表的软性毒品在自由城中一直受到保护和追捧。自由城中的大麻交易集中在城中的 Pusher Street. 下图街道两边的亭子里就是大麻的销售场所。 在 Pusher Street 有三条规定：“have fun”、“No photo”和“Do not run”。
曾在自由城的一处自制建筑上看到这样一段话（T.E.Lawrence 的名言）：All men dream: but not equally. Those who dream by night in the dusty recesses of their minds wake in the day to find that it was vanity: but the dreamers of the day are dangerous men, for they may act their dreams with open eyes, to make it possible.
自由城的居民喜爱艺术，单单是音乐厅，在自由城内就有好几个，有室内的也有露天的。其中最著名的当属 Grey hall， 这座音乐厅始建于 1891 年，可容纳数千人。与自由城内的居民聊天，他们自豪的告诉我：鲍勃迪伦、绿日乐队、blur 等等知名的乐队和歌手都曾经在自由城表演过。现在，每周依然会有来自世界各地的艺术家在自由城内的各个音乐厅表演。
也许自由城的居民们都是白日梦想家，他们活在乌托邦的幻想里，但同时他们好像又成了实干家，他们竟把这幻想变为了现世，他们真的创造出了一个乌托邦。"""
text_2 = """曾有人在一处自制建筑上看到这样一段话: All men dream: but not equally. Those who dream by night in the dusty recesses of their minds wake in the day to find that it was vanity: but the dreamers of the day are dangerous men, for they may act their dreams with open eyes, to make it possible.也许自由城的居民们都是白日梦想家，他们活在乌托邦的幻想里，但同时他们好像又成了实干家，他们竟把这幻想变为了现世，他们真的创造出了一个乌托邦。"""
THRESHOLD = 0.15
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
