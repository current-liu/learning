#!/usr/bin/env python
# coding=utf-8
"""
Created on 2017/11/22 23:20

base Info
"""
import codecs
import jieba
import re
import numpy as np
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread

__author__ = 'liuchao'
__version__ = '1.0'


def get_text_from_db():
    conn = sqlite3.connect('%s' % 'MM.sqlite')  # 连接数据库
    cur = conn.cursor()


    # query = "SELECT name FROM sqlite_master WHERE type='table' order by name"  # 查询所有表名
    # a = pd.read_sql(query, conn)
    # result = []
    # for i in a.name: #开始遍历所有表查找女票(的聊天记录)藏身之处
    #     if result.__len__()!=0:
    #         break
    #     query3 = "SELECT * FROM %s" %(i)
    #     r = pd.read_sql(query3, conn)
    #     if 'Message' in r.columns:
    #         for j in r.Message:
    #             if 'buhaowan' in j: #注1，关键的一步
    #                 result.append(i)
    #
    # table = result[0]

    table = 'Chat_87ba2f5e9ded271c345f25952086584c'
    table = "Chat_96b41172406d3e1fdcd12d36b3134aa4"
    query4 = "SELECT * FROM %s" % table # 注1那步完成得好，result就会只有一个元素
    text = pd.read_sql(query4, conn)

    return text

text_df = get_text_from_db()

def output_file(chat_text):
    text = list(chat_text.Message)  # 注2
    full_text = '\n'.join(text)  # 将text这个列表合并成字符串，以回车符分隔
    f = open('chat.txt', 'w')
    f.write(full_text)
    f.close()

output_file(text_df)

def fenci(chat_text):


    file = codecs.open('chat.txt', 'r')
    content = file.read()
    file.close()
    segment = []
    segs = jieba.cut(content)  # 分词
    for seg in segs:
        if len(seg) > 1 and seg != '\r\n':
            segment.append(seg)

    words_df = pd.DataFrame({'segment': segment})
    del segment  # 将segment转换成DataFrame后删掉，释放内存
    return words_df
words_df = fenci(text_df)

def init_stopwords():
    exclusive = []  # 建立一个停用词列表
    # for i in words_stat.segment:
    #     if re.findall(r'[A-Za-z0-9]*', i)[0] != '':  # 通过正则式表达排除英文、数字。findall返回的是一个列表
    #         exclusive.append(i)

    # for j in ['666', '233', '2333', 'App', 'app', 'Mac', 'mac']:  # 我的举例，读者可自行添加
    #     exclusive.remove(j)  # 从排除列表中删去这些需要保留的词汇

    ex = ['撤回']  # 举例
    for e in ex:
        exclusive.append(e)

    stop = '\n'.join(exclusive)
    f = open('stopwords.txt', 'w')
    f.write(stop)
    f.close()

    stopwords1 = pd.read_csv("stop_0.txt", index_col=False, quoting=3, sep="\t", names=['stopword'], encoding="utf8")

    stopwords2 = pd.read_csv("stop_1.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                             encoding="utf8")  # 第三方停用词库

    stopwords = stopwords1.append(stopwords2)

    return stopwords

stopwords = init_stopwords()

words_df = words_df[~words_df.segment.isin(stopwords.stopword)]  # 用停用词库更新分词列表

def stat(words_df):
    # words_stat = words_df.groupby(by=['segment'])['segment'].agg({"total": pd.np.size})
    words_stat = words_df.groupby('segment').sum()
    # words_stat = pd.pivot_table(words_df, values='segment',columns='segment',aggfunc=np.sum)# 计算频率
    print(words_stat)
    words_stat = words_stat.reset_index().sort_values(by="total", ascending=False)

    file = codecs.open('chat.txt', 'r')
    content = file.read()
    file.close()
    segment = []
    segs = jieba.cut(content)  # 分词
    for seg in segs:
        if len(seg) > 1 and seg != '\r\n':
            segment.append(seg)

    words_df = pd.DataFrame({'segment': segment})
    del segment  # 将segment转换成DataFrame后删掉，释放内存

    bimg = imread('love.png')  # 背景图片
    wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", mask=bimg, max_font_size=600,
                          random_state=100)  # 背景设成白的比较合适，我感觉；max_font_size和random_state自己调咯
    wordcloud = wordcloud.fit_words(words_stat.head(4000).itertuples(index=False))  # 词频排名前多少的放到图里
    bimgColors = ImageColorGenerator(bimg)
    plt.figure()
    plt.imshow(wordcloud.recolor(color_func=bimgColors))
    plt.axis("off")
    plt.show()
    wordcloud.to_file("result.png")  # 存成文件

stat(words_df)