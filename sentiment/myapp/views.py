import _thread
import sys
import threading
import time
from sched import scheduler
import pandas as pd
import jieba
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Avg
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import BlogInfo
from .models import CreatorInfo
import create_creator_wordcloud
import get_supertopic
import create_supertopic_wordcloud
import cul_blog_sentiment


# Create your views here.


# 随django服务启动，开始爬取超话数据
def get_data():
    get_supertopic.get_supertopic()

# 计算微博情感值
def cul_blog_sentiment():
    '''计算微博的情感'''
    df = pd.read_table("E:\\Sentiment\\dataset\\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
    key = df['key'].values.tolist()
    score = df['score'].values.tolist()
    objs = BlogInfo.objects.filter(sentiment_score__isnull=True)
    # objs = BlogInfo.objects.all()
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
        elif sentiment_score < 0.4:
            sentiment = '消极'
        else:
            sentiment = '中性'
        # print(score,sentiment)
        BlogInfo.objects.filter(blog_id=blog_id).update(sentiment=sentiment,sentiment_score=sentiment_score)
        continue
    print('微博情感计算完毕')
# cul_blog_sentiment()

# try:
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), 'default')

    #
    # # 定时任务1，爬取微博抑郁症超话内容
    # # 固定时间执行
    # #装饰器的方式创建任务
    # @register_job(scheduler, "interval", minutes=30, id='get_data_task',replace_existing=True)
    # def get_data_task():
    #     print('任务一：获取超话内容')
    #     get_supertopic.get_supertopic()

# 注册定时任务并开始
# register_events(scheduler)
# scheduler.start()
# except Exception as e:
# print(e)
# scheduler.shutdown()
    #

    # schedule.every(1).minutes.doget_data_task)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
# 使用add_job函数的方式创建任务
# sched.add_interval_job(get_data_task, minutes=10)
# sched.start()

def cul_creator_sentiment():
    ''' 计算用户贴子数 & 计算超话用户情感 '''
    objs = CreatorInfo.objects.all()
    for obj in objs:
        avr = BlogInfo.objects.filter(creator_id=obj.creator_id).aggregate(Avg("sentiment_score"))
        avr_score = avr['sentiment_score__avg']
        blog_counts = BlogInfo.objects.filter(creator_id=obj.creator_id).count()
        CreatorInfo.objects.filter(creator_id=obj.creator_id).update(creator_sentiment_score=avr_score,blog_counts=blog_counts)
    topic_avr = CreatorInfo.objects.filter(creator_sentiment_score__isnull=False).aggregate(Avg("creator_sentiment_score"))
    topic_avr = topic_avr["creator_sentiment_score__avg"]
    for obj in objs:
        if obj.creator_sentiment_score:
            score = obj.creator_sentiment_score
        else:
            continue
        if score> topic_avr+1:
            sentiment = '积极'
        elif score< topic_avr-1:
            sentiment = '消极'
        else:
            sentiment = '中性'
        CreatorInfo.objects.filter(creator_id=obj.creator_id).update(creator_sentiment=sentiment)
    print('完成！！计算用户贴子数 & 计算用户情感')

# cul_creator_sentiment()

# 创建线程
# t1 = threading.Thread(target=get_data)
# t2 = threading.Thread(target=cul_blog_sentiment)
# # t3 = threading.Thread(target=cul_creator_sentiment)
#
# # 开启新线程
# t1.start()
# t2.start()
# # t3.start()
# t1.join()
# t2.join()
# t3.join()

def tp_wordcloud(request):
    ''' 调用生成超话词云图的程序，生成词云图，响应返回词云图 '''
    create_supertopic_wordcloud.create_supertopic_wordcloud()
    # imagepath = './dataset/tp_wordcloud.png'
    # tp_wc_img = open(imagepath,'rb').read()
    # return HttpResponse(tp_wc_img,content_type="image/png")

# def go_tp_wc_html(request):
#     ''' 将内容返回到超话词云页面 '''
#     return render(request, "myapp/tp_wordcloud.html", locals())

