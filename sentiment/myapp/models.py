from django.db import models

# Create your models here.
class BlogInfo(models.Model):
    blog_id = models.CharField(max_length=32)
    creator_nickname = models.CharField(max_length=64)
    blog_content = models.CharField(max_length=1024)
    creator_id = models.CharField(max_length=64)
    created_time = models.CharField(max_length=128)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sentiment = models.CharField(max_length=16, blank=True, null=True)


    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name
        db_table = 'blogs'

    def __str__(self):
        return self.creator_nickname,self.created_time

from django.db import models

# Create your models here.
class CreatorInfo(models.Model):
    creator_id = models.CharField(max_length=64)
    creator_nickname = models.CharField(max_length=64)
    creator_gender = models.CharField(max_length=16)
    blog_counts = models.IntegerField(blank=True, null=True)
    creator_sentiment = models.CharField(max_length=16, blank=True, null=True)
    creator_sentiment_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = '超话用户'
        verbose_name_plural = verbose_name
        db_table = 'supertopic_fans'

    def __str__(self):
        return self.creator_id,self.creator_nickname,self.creator_gender,self.c


