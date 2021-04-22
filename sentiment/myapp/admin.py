from django.contrib import admin

from .models import *
# Register your models here.

admin.site.site_title = '抑郁症超话文本情感分析系统'
admin.site.site_header = '抑郁症超话内容分析系统后台'
admin.site.index_title = '抑郁症超话内容情感分析系统'

#定义一个类，继承admin.ModelAdmin
class BlogInfoAdmin(admin.ModelAdmin):
    # 要显示的列表
    list_display = ['blog_content','creator_nickname', 'created_time', 'sentiment', 'sentiment_score']
    # 为列表页的昵称字段设置路由地址，该路由地址可进入内容页
    list_display_links = ['creator_nickname']

    # 设置列表页显示最大上限数据量
    list_max_show_all = 100
    # 设置每页显示数据量
    list_per_page = 10

    #设置可搜索的字段
    search_fields = ['creator_nickname']

    # 在数据新增页或修改页设置可编辑的字段
    fields = ['blog_content']
    #
    # # 在新增/修改页设置不可编辑的字段
    # exclude = []

class CreatorInfoAdmin(admin.ModelAdmin):
    # 要显示的列表
    list_display = ['creator_id','creator_nickname', 'creator_gender', 'creator_sentiment', 'creator_sentiment_score']
    # 为列表页的昵称字段设置路由地址，该路由地址可进入内容页
    list_display_links = []

    # 设置列表页显示最大上限数据量
    list_max_show_all = 100
    # 设置每页显示数据量
    list_per_page = 10

    #设置可搜索的字段
    search_fields = ['creator_nickname']

    # 在数据新增页或修改页设置可编辑的字段
    fields = []
    #
    # # 在新增/修改页设置不可编辑的字段
    # exclude = []
# 注册的时候要把类也添加进去
admin.site.register(BlogInfo,BlogInfoAdmin)
admin.site.register(CreatorInfo,CreatorInfoAdmin)