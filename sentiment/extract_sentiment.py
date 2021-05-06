import pandas as pd

def extract_blog_sentiment():
    '''提取关键情感词'''
    df = pd.read_table("E:\\Sentiment\\dataset\\负面情感词语（中文）.txt", header=None)
    key = df['key'].values.tolist()
    objs = BlogInfo.objects.filter(sentiment_score__isnull=True)
    for obj in objs:
        blog_content = obj.blog_content
        blog_id = obj.blog_id
        # print(blog_id)
        segs = jieba.lcut(blog_content, cut_all=False)  # 返回list，计算得分
        key_list = [key.index(x)for x in segs if (x in key)]
        # print(score,sentiment)
        BlogInfo.objects.filter(blog_id=blog_id).update(sentiment=sentiment)
        continue
    print('微博情感提取完毕')