from django.contrib import admin
from django.forms import Textarea

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
# class BlogInfoAdmin(admin.ModelAdmin):
#     # 要显示的列表
#     list_display = ['blog_content','creator_nickname', 'created_time','sentiment',]
#     readonly_fields = ['blog_content','creator_nickname', 'created_time', 'sentiment', 'sentiment_score']
#     # 为列表页的昵称字段设置路由地址，该路由地址可进入内容页
#     list_display_links = []
#     # 设置列表页显示最大上限数据量
#     list_max_show_all = 1000
#     # 设置每页显示数据量
#     list_per_page = 10
#     #设置可搜索的字段
#     search_fields = ['creator_nickname']
#     # 在数据新增页或修改页设置可编辑的字段
#     fields = ['blog_content','creator_nickname','created_time']
#     # 在新增/修改页设置不可编辑的字段
#     # exclude = ['creator_nickname','creator_id']
#     # 设置不显示批量操作
#     actions_on_bottom = False
#     actions_on_top = False
#     # 禁用添加按钮
#     def has_add_permission(self, request):
#         return False
#     # 禁用删除按钮
#     def has_delete_permission(self, request, obj=None):
#         return False
#     # def has_change_permission(self, request, obj=None):
#     #     return True
#     # def __str__(self):
#     #     return self.blog_content

class CreatorInfoAdmin(admin.ModelAdmin):
    # 要显示的列表
    list_display = ['creator_nickname', 'creator_id','creator_gender', 'creator_sentiment_score','remark_text']
    #
    readonly_fields = ['creator_nickname', 'creator_id','creator_gender', 'creator_sentiment_score']
    # 为列表页的昵称字段设置路由地址，该路由地址可进入内容页
    list_display_links = []
    # 设置列表页显示最大上限数据量
    list_max_show_all = 200
    # 设置每页显示数据量
    list_per_page = 10
    #设置可搜索的字段
    search_fields = ['creator_id','creator_nickname']
    # 在数据新增页或修改页设置可编辑的字段
    fields = ['creator_id','creator_nickname','creator_gender','remark_text']
    # # 在新增/修改页设置不可编辑的字段
    # exclude = ['blog_counts','creator_sentiment_score']
    # 改变某个字段的文本框
    formfield_overrides = {models.TextField:{'widget':Textarea(attrs={'rows':5, 'cols':20})},}
    # 控制选择计数器隐藏
    actions_selection_counter = False
    # 禁用添加按钮
    def has_add_permission(self, request):
        return False
    # 点击保存并继续编辑取消
    save_as_continue = False
    # 从编辑页返回列表页时保存过滤条件
    preserve_filters = True
    def has_change_permission(self, request, obj=None):
        return True
    # # 自定义函数给remark_text填充
    # def save_remark_text(self,request,obj,form,change):
    #     remark_text = request.POST.get('remark_text')
    #     obj.remark_text = remark_text
    #     obj.save()
    # def __str__(self):
    #     return self.creator_id
# 注册的时候要把类也添加进去
admin.site.register(BlogInfo)
admin.site.register(CreatorInfo,CreatorInfoAdmin)