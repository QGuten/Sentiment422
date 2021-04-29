"""sentiment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

import myapp
from myapp import views
from myapp.views import *

from sentiment.myapp.views import tp_wordcloud

urlpatterns = [
    # 页面配置
    path('', admin.site.urls),
    path('admin/', admin.site.urls),
    # 加入myapp应用的路径
    path('myapp/', include("myapp.urls")),
    # path('creator_woudcloud/', views.creator_wordcloud, name='creator_wc'),
    path('to_wordcloud', tp_wordcloud),
]
