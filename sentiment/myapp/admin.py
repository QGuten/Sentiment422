from django.contrib import admin
from django.forms import Textarea
from django.utils.html import format_html
import jieba
import jieba.analyse
import sys

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
    list_display = ['blog_content','creator_nickname', 'sentiment','blog_keyword']
    readonly_fields = ['blog_content','creator_nickname', 'created_time', 'sentiment', 'sentiment_score']
    # 为列表页的昵称字段设置路由地址，该路由地址可进入内容页
    list_display_links = []
    # 设置列表页显示最大上限数据量
    list_max_show_all = 1000
    # 设置每页显示数据量
    list_per_page = 10
    #设置可搜索的字段
    search_fields = ['creator_nickname','creator_id']
    # 在数据新增页或修改页设置可编辑的字段
    fields = ['blog_content','creator_nickname','created_time','sentiment', 'sentiment_score']
    # 设置不显示批量操作
    actions_on_bottom = False
    actions_on_top = False
    # 禁用添加按钮
    def has_add_permission(self, request):
        return False
    # 禁用删除按钮
    def has_delete_permission(self, request, obj=None):
        return False
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
    # 要显示的列表
    list_display = ['creator_nickname','creator_gender', 'blog_counts','remark_text','blogs_by']
    # 设置编辑页只读字段
    readonly_fields = ['creator_nickname', 'creator_id','creator_gender','blog_counts', 'creator_sentiment_score']
    # 为列表页的昵称字段设置路由地址，该路由地址可进入内容页
    list_display_links = []
    # 设置列表页显示最大上限数据量
    list_max_show_all = 100000000
    # 设置每页显示数据量
    list_per_page = 10
    #设置可搜索的字段
    search_fields = ['creator_id','creator_nickname']
    # 在数据新增页或修改页设置可编辑的字段
    fields = ['creator_id','creator_nickname','creator_gender','blog_counts', 'creator_sentiment_score', 'remark_text']
    # # 在新增/修改页设置不可编辑的字段
    # exclude = ['blog_counts','creator_sentiment_score']
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
        url_text = "ta的发帖"
        return format_html(u'<a href="{}" target="_blank">{}</a>'.format(url,url_text))
    blogs_by.allow_tags = True
    blogs_by.short_description = 'ta的发帖'

    # 添加词云页面入口
    # def creator_wordcloud(self,obj):
    #     url = "http://127.0.0.1:8000/myapp/creatorinfo/%s"%obj.creator_id
    #     url_text = 'ta的词云'
    #     return format_html(u'<a href="{}" target=_blank">{}</a>'.format(url,url_text))
    # creator_wordcloud.allow_tags = True
    # creator_wordcloud.short_description = 'ta的词云'

    # 添加自定义按钮
    # actions = ['blogs_by_creator']
    # def blogs_by_creator(self, request):
    #     return True
    # # 自定义按钮的配置
    # blogs_by_creator.shor_description = 'ta的发布的超话帖子'
    # blogs_by_creator.icon = 'el-icon-video-pause'
    # blogs_by_creator.type = 'danger'
    # blogs_by_creator.style = 'color:rainbow;'
    # blogs_by_creator.action_type = 0    #当前页面打开
    # blogs_by_creator.action_url = 'blogsByCreator'
    # # 为微博数量添加超链接
    # def blog_counts(self,obj):
    #     return format_html("<a href='http://127.0.0.1:8000/myapp/bloginfo/?q={0}'>{0}</a>", obj.creator_nickname)
    # blog_counts.short_description = "ta的超话发言"

# 注册的时候要把类也添加进去
admin.site.register(BlogInfo,BlogInfoAdmin)
admin.site.register(CreatorInfo,CreatorInfoAdmin)