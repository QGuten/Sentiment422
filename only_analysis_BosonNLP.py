# -*- coding:utf-8 -*-
import pandas as pd
import jieba

def csv_to_txt(csv_filename):
    data = pd.read_csv('dataset/neg.csv',encoding='utf-8')
    # data = data.drop('blog_id', axis = 1)
    # data = data.drop('nick_name', axis = 1)
    with open('dataset/neg.txt', 'a+', encoding='utf-8') as f:
        for line in data.values:
            # line = filter(lambda ch: ch not in'\t1234567890abcdefghijklmnopqrstuvwxyz-_?()@#!`~',line)    # 需要清洗数字、英文、字符，待完善
            f.write(str(line)+'\n')

# 停词函数
def get_custom_stopword(stop_word_file):
    with open(stop_word_file) as f:
        stop_word = f.read()

    stop_word_file = stop_word.split("/n")
    custom_stopword = [i for i in stop_word_file]
    return custom_stopword

# 基于波森情感词典计算情感值
def getscore(text):
    df = pd.read_table(r"dataset\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
    key = df['key'].values.tolist()
    score = df['score'].values.tolist()
    # jieba分词
    segs = jieba.lcut(text, cut_all=False)  # 返回list
    # 计算得分
    score_list = [score[key.index(x)] for x in segs if (x in key)]
    return sum(score_list)


# 读取文件
def read_txt(filename):
    with open(filename, 'r', encoding='utf-8')as f:
        txt = f.read()
    return txt

# 写入文件
def write_data(filename, data):
    with open(filename, 'a', encoding='utf-8')as f:
        f.write(data)


if __name__ == '__main__':
    csv_file = 'dataset/neg.csv'
    csv_to_txt('csv_file')

    text = read_txt('dataset/neg.txt')
    lists = text.split('\n')

    # al_senti = ['无','积极','消极','消极','中性','消极','积极','消极','积极','积极','积极','无','积极','积极','中性','积极','消极','积极','消极','积极','消极','积极','无','中性','消极','中性','消极','积极','消极','消极','消极','消极','积极']

    # al_senti = read_txt(r'dataset/人工情感标注.txt').split('\n')
    i = 0
    for list in lists:
        if list != '':
            # print(list)
            sentiments = round(getscore(list), 2)
            # 情感值为正数，表示积极；为负数表示消极
            print(list)
            print("情感值：", sentiments)
            # print('人工标注情感倾向：' + al_senti[i])
            if sentiments > 0:
                print("机器标注情感倾向：积极\n")
                s = "积极"
            else:
                print('机器标注情感倾向：消极\n')
                s = "消极"
            sentiment = '情感值：' + str(sentiments) + '\n'
            # al_sentiment = '人工标注情感倾向:' + al_senti[i] + '\n'
            # 文件写入
            filename = 'dataset/BosonNLP_analysis_result.txt'
            write_data(filename, '情感分析文本：')
            write_data(filename, list + '\n')  # 写入待处理文本
            write_data(filename, sentiment)  # 写入情感值
            # write_data(filename, al_sentiment)  # 写入机器判断情感倾向
            # write_data(filename, s + '\n')  # 写入人工标注情感
            i = i + 1