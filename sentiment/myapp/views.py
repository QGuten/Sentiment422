import _thread
import sys
import threading
import time
from sched import scheduler
import pandas as pd
import jieba
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.db.models import Avg
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import BlogInfo
from .models import CreatorInfo
import create_creator_wordcloud
import get_supertopic
import create_supertopic_wordcloud
import cul_blog_sentiment


# Create your views here.
try:
    job_defaults = {'max_instances':4}
    scheduler = BackgroundScheduler(job_defaults=job_defaults)
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    # 定时任务1，爬取微博抑郁症超话内容,固定时间执行
    #装饰器的方式创建任务
    @register_job(scheduler, "interval", hours=2, id='get_data',replace_existing=True)
    def get_data():
        time.sleep(2)
        get_supertopic.get_supertopic()


    # 定时任务2，间隔性任务，计算还未计算过情感的微博的情感
    @register_job(scheduler, "interval", minutes=30, id='get_blog_sentiment', replace_existing=True)
    def get_blog_sentiment():
        cul_blog_sentiment()

    # 定时任务3，更新超话用户帖子数目及个人情感
    @register_job(scheduler, "cron", hour=14,minute=16,id='get_creator_sentiment', replace_existing=True)
    def get_creator_sentiment():
        cul_creator_sentiment()

    # 监控任务
    register_events(scheduler)
    # 调度器开始
    scheduler.start()
except Exception as e:
    print(e)
    scheduler.shutdown()
    pass

# 计算微博情感值
def cul_blog_sentiment():
    '''计算微博的情感'''
    df = pd.read_table("E:\\Sentiment\\dataset\\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
    key = df['key'].values.tolist()
    score = df['score'].values.tolist()
    objs = BlogInfo.objects.filter(sentiment_score__isnull=True)
    for obj in objs:
        blog_content = obj.blog_content
        # print(blog_content)
        blog_id = obj.blog_id
        # print(blog_id)
        segs = jieba.lcut(blog_content, cut_all=False)  # 返回list，计算得分
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
# # 开启新线程
# t1.start()
# t1.join()

def tp_wordcloud(request):
    ''' 调用生成超话词云图的程序，生成词云图，响应返回词云图 '''
    create_supertopic_wordcloud.create_supertopic_wordcloud()
    # imagepath = './dataset/tp_wordcloud.png'
    # tp_wc_img = open(imagepath,'rb').read()
    return redirect('myapp/bloginfo')


