import sys
import pandas as pd
import jieba
import schedule
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
# from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
import time

# from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events

sys.path.append(r'E:\Sentiment')

from .models import BlogInfo
from .models import CreatorInfo
import get_supertopic as g

# Create your views here.
# try:
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), 'default')
#
#     #定时任务1，爬取微博抑郁症超话内容
#     # 固定时间执行
#     # @register_job(scheduler, 'cron', id='test', hour=8, minute=3,args=['scratpyDataTask'])   # 装饰器的方式创建任务
#     @register_job(scheduler, "interval", minutes=5, id='get_data_task',replace_existing=True)
#     def get_data_task():
#         print('任务一：获取超话内容')
#         g.get_supertopic()
#
#
#     @register_job(scheduler, "interval", minutes=5,id='cul_fan_blogs',  replace_existing=True)
#     def cul_fan_blogs():
#         '''计算某作者贴子数（计算爬取到的）'''
#         print('任务二：计算微博数量')
#         creators_list=CreatorInfo.objects.values_list('creator_id', flat=True)
#         for creator in creators_list:
#             counts = BlogInfo.objects.filter(creator_id=creator).count()
#             CreatorInfo.objects.filter(creator_id=creator).update(blog_counts=counts)
#
#     # 注册定时任务并开始
#     register_events(scheduler)
#     scheduler.start()
# except Exception as e:
#     print(e)
#     scheduler.shutdown()
    #
    # #定时任务2，计算帖子的情感
    # def culBlogSentimentTask():
    #     print('计算文本情感')
    #

    # schedule.every(1).minutes.doget_data_task)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # 使用add_job函数的方式创建任务
    # sched.add_interval_job(get_data_task, minutes=10)
    # sched.start()

def blogDetail(request, id):
    try:
        blog = BlogInfo.objects.filter(pk=id).first()
    except CreatorInfo.DoesNotExist:
        raise Http404('不存在')
    return render(request,'blogDetail.html',{'blog':blog})

# def supertopic_wordcloud(request):

# 随django服务启动，开始爬取超话数据
# g.get_supertopic()

def cul_fan_blogs():
    '''计算某作者贴子数（计算爬取到的）'''
    print('任务二：计算微博数量')
    creators_list=CreatorInfo.objects.values_list('creator_id', flat=True)
    for creator in creators_list:
        if creator:
            counts = BlogInfo.objects.filter(creator_id=creator).count()
            print('计算中：%d'%counts)
            CreatorInfo.objects.filter(creator_id=creator).update(blog_counts=counts)
        else:
            print('计算结束')
#
# def cul_blog_sentiment():
#     '''计算微博的情感'''
#     df = pd.read_table("E:\\Sentiment\\dataset\\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
#     key = df['key'].values.tolist()
#     score = df['score'].values.tolist()
#     objs = BlogInfo.objects.filter(sentiment_score__isnull=True)
#     # print(objs)
#     for obj in objs:
#         blog_content = obj.blog_content
#         # print(blog_content)
#         blog_id = obj.blog_id
#         # print(blog_id)
#         segs = jieba.lcut(blog_content, cut_all=False)  # 返回list
#         # 计算得分
#         score_list = [score[key.index(x)] for x in segs if (x in key)]
#         sentiment_score = sum(score_list)
#         if sentiment_score >30:
#             sentiment = '积极'
#         elif sentiment_score < -7:
#             sentiment = '消极'
#         else:
#             sentiment = '中性'
#         # print(score,sentiment)
#         BlogInfo.objects.filter(blog_id=blog_id).update(sentiment=sentiment,sentiment_score=sentiment_score)
#         continue
#     print('计算完毕')
#
# cul_blog_sentiment()