from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader, RequestContext, Context
import requests
from urllib.parse import urlencode

import jsonpath
from .models import BlogInfo
from .models import CreatorInfo

# Create your views here.
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
    


def cul_fan_blogs(request,creator_id):
    creator= BlogInfo.objects.filter(creator_id=creator_id)
    creator.blog_counts = BlogInfo.objects.filter(creator_id).counts()
    creator.save()
