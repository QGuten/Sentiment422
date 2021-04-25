from django.db import models

# Create your models here.
class BlogInfo(models.Model):
    blog_id = models.CharField(max_length=32,blank=True,null=True)
    creator_nickname = models.CharField(max_length=64,verbose_name='用户昵称')
    blog_content = models.CharField(max_length=1024,verbose_name='微博文本')
    creator_id = models.CharField(max_length=64,verbose_name='用户微博ID')
    created_time = models.CharField(max_length=128,blank=True,null=True,verbose_name='微博发布时间')
    sentiment = models.CharField(max_length=16, blank=True, null=True,verbose_name='微博情感偏向')
    sentiment_score = models.FloatField(blank=True, null=True,verbose_name='微博情感分值')

    class Meta:
        verbose_name = '超话帖子'
        verbose_name_plural = verbose_name
        db_table = 'blogs'

    def __str__(self):
        return self.blog_content


# 粉丝模型
class CreatorInfo(models.Model):
    creator_id = models.CharField(max_length=64,verbose_name='用户微博ID')
    creator_nickname = models.CharField(max_length=64,verbose_name='用户昵称')
    creator_gender = models.CharField(max_length=16,verbose_name='用户性别')
    blog_counts = models.IntegerField(blank=True, null=True,verbose_name='用户超话发帖数')
    creator_sentiment = models.CharField(max_length=16, blank=True, null=True,verbose_name='用户情感偏向')
    creator_sentiment_score = models.FloatField(blank=True, null=True,verbose_name='用户情感分值')
    remark_text = models.CharField(max_length=2048,blank=True, null=True,verbose_name='备注')

    class Meta:
        verbose_name = '超话用户'
        verbose_name_plural = verbose_name
        db_table = 'supertopic_fans'

    def __str__(self):
        return self.creator_nickname

