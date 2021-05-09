import _thread
import json
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

from .models import BlogInfo, CustomText
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
    @register_job(scheduler, "interval", hours=20, id='获取微博超话信息',replace_existing=True)
    def get_data():
        time.sleep(2)
        get_supertopic.get_supertopic()

    # 定时任务，更新情感为中性的微博情感
    # @register_job(scheduler, 'interval' , minutes=10, id='分析帖子情感', replace_existing=True)
    # def get_sentiment():
    #     extract_blog_sentiment()

    # 定时任务3，更新超话用户帖子数目及个人情感
    @register_job(scheduler, "cron", hour=20,minute=30,id='计算超话粉丝情感倾向及发帖次数', replace_existing=True)
    def get_creator_sentiment():
        cul_creator_sentiment()

    register_events(scheduler)      # 监控任务
    scheduler.start()       # 调度器开始
except Exception as e:
    print(e)
    scheduler.shutdown()
    pass

def extract_blog_sentiment():
    '''提取关键情感词'''
    file_nocut = 'E:\\Sentiment\\sentiment\\dataset\\nocut.txt'
    jieba.load_userdict(file_nocut)
    df = pd.read_table("E:\\Sentiment\\sentiment\\dataset\\情感词.txt", sep='\n', header=None, encoding='gbk')
    df.columns=['key']
    keys = df['key'].values.tolist()
    for i in range(len(keys)):
        keys[i] = keys[i].replace(' ','')
    BSdf = pd.read_table("E:\\Sentiment\\dataset\\BosonNLP_sentiment_score.txt", sep=" ",
                         names=['BSkey', 'BSscore'])
    BSkey = BSdf['BSkey'].values.tolist()
    BSscore = BSdf['BSscore'].values.tolist()
    objs = BlogInfo.objects.filter(sentiment_score__isnull=True)
    for obj in objs:
        blog_content = obj.blog_content
        blog_id = obj.blog_id
        print(blog_id)
        segs = jieba.lcut(blog_content, cut_all=True, HMM=False)  # 返回list，计算得分
        score_list = [BSscore[BSkey.index(x)] for x in segs if (x in BSkey)]
        sentiment_score = sum(score_list)
        xx = '未知'
        for x in segs:
            print('x是:%s'%x)
            if x in keys:
                xx = x
                sentiment = xx
                print('xx为:%s'%xx)
                BlogInfo.objects.filter(blog_id=blog_id).update(sentiment=sentiment, sentiment_score=sentiment_score)
                print('句子中有明显情感：%s'%sentiment)
        if xx!='未知':
            continue
        else:
                if sentiment_score > 30:
                    sentiment = '积极'
                elif sentiment_score < 0:
                    sentiment = '消极'
                else:
                    sentiment = '中性'
                print('sentiment情感是:%s'%sentiment)
        # print(score,sentiment)
                BlogInfo.objects.filter(blog_id=blog_id).update(sentiment=sentiment,sentiment_score=sentiment_score)
    print('微博情感提取完毕')
# extract_blog_sentiment()

def cul_creator_sentiment():
    ''' 计算用户贴子数 & 计算超话用户情感 '''
    print('计算用户贴子数 & 计算超话用户情感')
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
cul_creator_sentiment()

def tp_wordcloud(request):
    ''' 调用生成超话词云图的程序，生成词云图，响应返回词云图 '''
    text_list = BlogInfo.objects.values_list('blog_content', flat=True)
    create_supertopic_wordcloud.create_supertopic_wordcloud(text_list)
    # imagepath = './dataset/tp_wordcloud.png'
    # tp_wc_img = open(imagepath,'rb').read()
    return redirect('http://127.0.0.1:8000/myapp/bloginfo/')

sentiment='未知'
sentiment_score=0
def cul_text_sentiment(request):
    '''计算自定义输入内容的情感'''
    global sentiment
    global sentiment_score
    file_nocut = 'E:\\Sentiment\\sentiment\\dataset\\nocut.txt'
    jieba.load_userdict(file_nocut)
    df = pd.read_table("E:\\Sentiment\\sentiment\\dataset\\情感词.txt", sep='\n', header=None, encoding='gbk')
    df.columns=['key']
    keys = df['key'].values.tolist()
    for i in range(len(keys)):
        keys[i] = keys[i].replace(' ','')
    BSdf = pd.read_table("E:\\Sentiment\\dataset\\BosonNLP_sentiment_score.txt", sep=" ", names=['BSkey', 'BSscore'])
    BSkey = BSdf['BSkey'].values.tolist()
    BSscore = BSdf['BSscore'].values.tolist()
    if request.method == 'POST':
        customtext = request.POST.get('customtext')
        segs = jieba.lcut(customtext, cut_all=False, HMM=False)  # 返回list，计算得分
        xx = '未知'
        for x in segs:
            print('x是:%s'%x)
            score_list = [BSscore[BSkey.index(x)] for x in segs if (x in BSkey)]
            sentiment_score = sum(score_list)
            if x in keys:
                xx = x
                sentiment = xx
                print('句子中有明显情感：%s'%sentiment)
        if xx=='未知':
                if sentiment_score > 30:
                    sentiment = '积极'
                elif sentiment_score < 0:
                    sentiment = '消极'
                else:
                    sentiment = '中性'
        data = {'sentiment':sentiment,'sentiment_score':sentiment_score}
        json_data = json.dumps(data)
        # print('结果为：%s,%s'%(sentiment_score,sentiment))
        return render(request, 'myapp/custom_text.html', {'sentiment': sentiment, 'sentiment_score': sentiment_score})
    return render(request, 'myapp/custom_text.html',{'sentiment':sentiment,'sentiment_score':sentiment_score})

#