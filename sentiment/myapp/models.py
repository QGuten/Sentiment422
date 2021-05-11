from django.db import models

# Create your models here.
class BlogInfo(models.Model):
    blog_id = models.CharField(primary_key=True,max_length=32,blank=True)
    creator_nickname = models.CharField(max_length=32,blank=True,null=True,verbose_name='帖子发布者昵称')
    creator_id = models.CharField(max_length=64,default='超级管理员',verbose_name='帖子发布者ID')
    blog_content = models.CharField(max_length=1024, verbose_name='帖子文本')
    created_time = models.CharField(max_length=128,blank=True,null=True,verbose_name='帖子发布时间')
    sentiment = models.CharField(max_length=16, blank=True, null=True,verbose_name='帖子情绪偏向')
    sentiment_score = models.FloatField(blank=True, null=True,verbose_name='帖子情感分值')

    class Meta:
        verbose_name = '抑郁症超话帖子'
        verbose_name_plural = verbose_name
        db_table = 'blogs'

    def __str__(self):
        return self.blog_content

# 粉丝模型
class CreatorInfo(models.Model):
    creator_id = models.CharField(primary_key=True,max_length=64,verbose_name='粉丝微博ID')
    creator_nickname = models.CharField(max_length=64,verbose_name='粉丝昵称')
    creator_gender = models.CharField(max_length=64,null=True,verbose_name='粉丝性别',default='f')
    blog_counts = models.IntegerField(blank=True, null=True,verbose_name='粉丝超话下总发帖数')
    worse_counts = models.IntegerField(blank=True, null=True,verbose_name='粉丝超话下比较消极帖子数')
    extreme_counts = models.IntegerField(blank=True, null=True,verbose_name='粉丝超话下非常消极帖子数')
    creator_sentiment = models.CharField(max_length=16, blank=True, null=True,verbose_name='粉丝情绪倾向')
    creator_sentiment_score = models.FloatField(blank=True, null=True,verbose_name='粉丝情感分值')
    remark_text = models.CharField(max_length=2048,blank=True, null=True,verbose_name='备注')

    class Meta:
        verbose_name = '抑郁症超话粉丝'
        verbose_name_plural = verbose_name
        db_table = 'supertopic_fans'

    def __str__(self):
        return self.creator_nickname

# 虚拟模型，承载超话词云
class TopicWord(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.CharField( max_length=10, verbose_name='超话关键词')
    count = models.CharField(max_length=7, verbose_name='超话关键词词频')
    class Meta:
        verbose_name = '抑郁症超话关键词'
        verbose_name_plural = verbose_name
        db_table = 'topic_keywords'

    def __str__(self):
        return self.keyword

class CustomText(models.Model):
    custom_content = models.TextField(verbose_name='文本')
    text_sentiment = models.CharField(max_length=10,blank=True, null=True, verbose_name='情绪倾向')
    text_sentiment_score = models.FloatField(blank=True, null=True, verbose_name='情感分值')

    class Meta:
        verbose_name = '自定义分析'
        verbose_name_plural = verbose_name
        db_table = 'custom_texts'

    def __str__(self):
        return self.content
