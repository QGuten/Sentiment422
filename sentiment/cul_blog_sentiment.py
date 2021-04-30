import pymysql
import pandas as pd
import jieba

from myapp.models import BlogInfo

def cul_blog_sentiment():
    '''计算微博的情感'''
    df = pd.read_table("E:\\Sentiment\\dataset\\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
    key = df['key'].values.tolist()
    score = df['score'].values.tolist()
    objs = BlogInfo.objects.filter(sentiment_score__isnull=True)
    # print(objs)
    for obj in objs:
        blog_content = obj.blog_content
        # print(blog_content)
        blog_id = obj.blog_id
        # print(blog_id)
        segs = jieba.lcut(blog_content, cut_all=False)  # 返回list
        # 计算得分
        score_list = [score[key.index(x)] for x in segs if (x in key)]
        sentiment_score = sum(score_list)
        if sentiment_score >30:
            sentiment = '积极'
        elif sentiment_score < -7:
            sentiment = '消极'
        else:
            sentiment = '中性'
        # print(score,sentiment)
        BlogInfo.objects.filter(blog_id=blog_id).update(sentiment=sentiment,sentiment_score=sentiment_score)
        continue
    print('计算完毕')
