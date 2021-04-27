import sys

import schedule
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
import time

from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events

sys.path.append(r'E:\Sentiment')

from .models import BlogInfo
from .models import CreatorInfo
import get_supertopic as g

# Create your views here.
try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    #定时任务1，爬取微博抑郁症超话内容
    # 固定时间执行
    # @register_job(scheduler, 'cron', id='test', hour=8, minute=3,args=['scratpyDataTask'])   # 装饰器的方式创建任务
    @register_job(scheduler, "interval", minutes=5, id='get_data_task',replace_existing=True)
    def get_data_task():
        print('任务一：获取超话内容')
        g.get_supertopic()


    @register_job(scheduler, "interval", minutes=5,id='cul_fan_blogs',  replace_existing=True)
    def cul_fan_blogs():
        '''计算某作者贴子数（计算爬取到的）'''
        print('任务二：计算微博数量')
        creators_list=CreatorInfo.objects.values_list('creator_id', flat=True)
        for creator in creators_list:
            counts = BlogInfo.objects.filter(ceator_id=creator).count()
            CreatorInfo.objects.filter(creator_id=creator).update(blog_counts=counts)

    # 注册定时任务并开始
    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    scheduler.shutdown()
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

def bloglist(request):
    bloglist = BlogInfo.objects.all()
    return render(request,bloglist)

def fanlist(request):
    fanlist = CreatorInfo.objects.all()
    return render(request,fanlist)

def detail(request, id):
    try:
        fan = CreatorInfo.objects.filter(pk=id).first()
    except CreatorInfo.DoesNotExist:
        raise Http404('不存在')
    return render(request,'index.html',{'fan':fan})

def blogDetail(request, id):
    try:
        blog = BlogInfo.objects.filter(pk=id).first()
    except CreatorInfo.DoesNotExist:
        raise Http404('不存在')
    return render(request,'blogDetail.html',{'blog':blog})

def addRemark(request,id):
    creator = get_object_or_404(CreatorInfo,pk=id)
    try:
        remark_text = creator.get(pk=request.POST['remark_text'])
    except:
        return render(request,'myapp/creator_profile.html',{'creator':creator,'error_message':"Could not remark.",})
    else:
        remark_text.save()
        return HttpResponseRedirect(args=(creator.id,))

# def supertopic_wordcloud(request):
    
def blogs_by_creator(request,creator_id):
    blogs = BlogInfo.objects.filter(creator_id=creator_id)
    return render(request,'bolgs_by_creator.html',{'blogs':blogs})


