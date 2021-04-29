import sys
import pandas as pd
import jieba
import schedule
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
# from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Avg
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
# from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events
import time

from .models import BlogInfo
from .models import CreatorInfo
sys.path.append(r'E:\Sentiment')

# import get_supertopic
import create_supertopic_wordcloud
# import cul_blog_sentiment


# Create your views here.

# def supertopic_wordcloud(request):

# 随django服务启动，开始爬取超话数据
# get_supertopic.get_supertopic()

# 计算微博情感值
# def cul_blog_sentiment():
#     '''计算微博的情感'''
#     df = pd.read_table("E:\\Sentiment\\dataset\\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
#     key = df['key'].values.tolist()
#     score = df['score'].values.tolist()
#     # objs = BlogInfo.objects.filter(sentiment_score__isnull=True)
#     objs = BlogInfo.objects.all()
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
#         elif sentiment_score < 0.4:
#             sentiment = '消极'
#         else:
#             sentiment = '中性'
#         # print(score,sentiment)
#         BlogInfo.objects.filter(blog_id=blog_id).update(sentiment=sentiment,sentiment_score=sentiment_score)
#         continue
#     print('计算完毕')
# cul_blog_sentiment()

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
#        g.get_supertopic()

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

def cul_creator_sentiment():
    ''' 计算用户 & 贴子数计算超话用户情感 '''
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
    print('完成！！计算用户贴子数 & 计算超话用户情感')
# cul_creator_sentiment()

def blogDetail(request, id):
    try:
        blog = BlogInfo.objects.filter(pk=id).first()
    except CreatorInfo.DoesNotExist:
        raise Http404('不存在')
    return render(request,'blogDetail.html',{'blog':blog})

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
# cul_fan_blogs()

def tp_wordcloud(request):
    ''' 调用生成超话词云图的程序，生成词云图，响应返回词云图 '''
    create_supertopic_wordcloud.create_supertopic_wordcloud()
    imagepath = 'E:\\Sentiment\\dataset\\tp_wordcloud.png'
    tp_wc_img = open(imagepath,'rb').read()
    return HttpResponse(tp_wc_img,content_type="image/png")

def go_tp_wc_html(request):
    ''' 将内容返回到超话词云页面 '''
    return render(request,"myapp/tp_wordcloud.html",locals())

