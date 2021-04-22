from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext, Context
import requests
from urllib.parse import urlencode

import jsonpath
from .models import BlogInfo
from .models import CreatorInfo

# Create your views here.
def index(request):
    return render(request, "myapp/index.html")

def showBlogs(request):
    blogs = BlogInfo.objects.values('blog_content', 'creator_nickname')
    return HttpResponse(blogs)

def showCreators(request):
    creators = CreatorInfo.objects.all()
    return HttpResponse(creators)

def api_wy(request):
    api = BlogInfo.objects.all()
    return render(request, 'index.html',locals())
