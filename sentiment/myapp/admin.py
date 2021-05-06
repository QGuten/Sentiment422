from django.contrib import admin
from django.forms import Textarea
from django.utils.html import format_html
import jieba
import jieba.analyse
import sys
import pandas as pd

import create_creator_wordcloud
from .forms import CreatorInfoAdminForm
from .models import *
# Register your models here.

admin.site.site_title = '抑郁症超话情感分析系统'
admin.site.site_header = '抑郁症超话情感分析系统'
admin.site.index_title = '抑郁症超话情感分析系统'

# 定制表单
# class MyForm(forms.ModelForm):
#     code = forms.CharField(validators=[validate], widget=forms.TextInput(attrs={'placeholder': u'输入四位数字填充字段C'}))
#
#     class Meta: # 不展示字段C
#         exclude = ['C']

#定义一个类，继承admin.ModelAdmin
class BlogInfoAdmin(admin.ModelAdmin):
    # 要显示的列表
    list_display = ['blog_content','creator_nickname','blog_keyword']
    fieldsets = (('基本信息', {'fields':('creator_id','creator_nickname','created_time')}),('其它',{'fields':('sentiment_score','sentiment')}))
    readonly_fields = ['blog_content','creator_nickname', 'creator_id', 'created_time', 'sentiment_score']
    # 为列表页的昵称字段设置路由地址，该路由地址可进入内容页
    list_display_links = []
    # 设置列表页显示最大上限数据量
    list_max_show_all = 1000
    # 设置每页显示数据量
    list_per_page = 10
    #设置可搜索的字段
    search_fields = ['creator_nickname','creator_id']
    # 设置不显示批量操作
    actions_on_bottom = False
    actions_on_top = False
    # 禁用添加按钮
    def has_add_permission(self, request):
        return False
    # 禁用删除按钮
    # def has_delete_permission(self, request, obj=None):
    #     return False
    # 生成自定义列关键词
    def blog_keyword(self, obj):
        stopwords_file = 'E:\\Sentiment\\dataset\\stopword2.txt'
        jieba.analyse.set_stop_words(stopwords_file)
        blog_content = obj.blog_content
        keyword = jieba.analyse.extract_tags(blog_content, topK=3)
        # print(keyword)
        return keyword
    blog_keyword.allow_tags = True
    blog_keyword.short_description = '关键词'

class CreatorInfoAdmin(admin.ModelAdmin):
    ''' 用户管理模型 '''
    form = CreatorInfoAdminForm
    # 要显示的列表
    list_display = ['creator_nickname', 'gender','blog_counts','remark_text','blogs_by',] # ,,'creator_wordcloud'
    # 设置编辑页只读字段
    readonly_fields = ['creator_nickname', 'creator_id','gender','blog_counts', 'creator_sentiment_score']
    # 为列表页的昵称字段设置路由地址，该路由地址可进入内容页
    # list_display_links = []
    # 设置列表页显示最大上限数据量
    list_max_show_all = 10000000
    # 设置每页显示数据量
    list_per_page = 10
    #设置可搜索的字段
    search_fields = ['creator_id','creator_nickname']
    fieldsets = (('基本信息', {'fields':('creator_id','creator_nickname','gender')}),('超话活跃情况',{'fields':('blog_counts','creator_sentiment_score','creator_sentiment')}),('其它',{'fields':('remark_text',),}))
    # 点击保存并继续编辑取消
    save_as_continue = False
    # 从编辑页返回列表页时保存过滤条件
    preserve_filters = True
    # 改变某个字段的文本框
    formfield_overrides = {models.TextField:{'widget':Textarea(attrs={'rows':5, 'cols':20})},}
    # 控制选择计数器隐藏
    actions_selection_counter = False
    # list_filter = ['atitle','aParent'] # 【8】列表页右侧过滤栏
    # 禁用添加按钮
    def has_add_permission(self, request):
        return False
    # 允许修改
    def has_change_permission(self, request, obj=None):
        return True

    # 添加自定义超链接列字段
    def blogs_by(self,obj):
        url = "http://127.0.0.1:8000/myapp/bloginfo/?q=%s"% obj.creator_nickname
        url_text = "ta的发言"
        return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url,url_text))
    # blogs_by.allow_tags = True
    blogs_by.short_description = 'ta的发言'

    # 性别转换中文
    def gender(self,obj):
        g = obj.creator_gender
        if g=='f':
            gender='女';
        else:
            gender = '男';
        return gender
    gender.short_description = '用户性别'

# # 自定义超链接产生用户词云图，实时生成
    def creator_wordcloud(self,obj):
        ''' 调用生成用户词云图的程序，生成词云图，响应返回词云图 '''
        blogs = BlogInfo.objects.filter(creator_id=obj.creator_id)
        for blog in blogs:
            text = '。'.join(blog.blog_content)
        create_creator_wordcloud.create_creator_wordcloud(text)
        # url = "http://127.0.0.1:8000/myapp/creatorinfo/%s/change" % obj.creator_id
        # url_text = "ta的词云"
        # return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url, url_text))
        return true
    creator_wordcloud.icon = 'el-icon-video-pause'
    creator_wordcloud.type = 'danger'
    creator_wordcloud.style = 'color:rainbow;'
    creator_wordcloud.short_description = 'ta的词云'


# 注册的时候要把类也添加进去
admin.site.register(BlogInfo,BlogInfoAdmin)
admin.site.register(CreatorInfo,CreatorInfoAdmin)

@admin.register(TopicWord)
class TopicWordAdmin(admin.ModelAdmin):
    # 要显示的列表
    list_display = ['keyword','count',]
    list_display_links = None
    list_max_show_all = 10000000
    list_per_page = 10
    search_fields = ['keyword',]
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CustomTextAdmin(admin.ModelAdmin):
    # 要显示的列表
    list_display = ['custom_content','text_sentiment',]
    list_display_links = ['custom_content']
    list_max_show_all = 10000000
    list_per_page = 10
    search_fields = ['custom_content','text_sentiment']
    readonly_fields = ['text_sentiment_score']

admin.site.register(CustomText,CustomTextAdmin)
