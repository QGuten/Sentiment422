import jieba
import jieba.analyse
import time
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image
import pymysql
import matplotlib.pyplot as plt

# def getText():
# 	 # 连接数据库
#     db = pymysql.connect(host="localhost", port=3306,database="sentiment", user="root",password="newpassword", charset='utf8')
#     try:
#         # 使用cursor()方法获取操作游标
#         cursor = db.cursor()
#         print('游标建立成功')
#         # 获取微博内容数据
#         sql = "select blog_content from blogs;"
#         cursor.execute(sql)
#         # 直接通过数据库查询获取的是((1,张三,男),(2,李四,女))这样的元组格式：
#         # 每条记录通过元组记录属性值，同时每条记录作为一个元组元素组成查询结果元组
#         results = cursor.fetchall()
#         # 将微博内容放入contents列表
#         contents = []
#         for re in results:
#         	#只取了text属性值，可直接extend
#             contents.extend(re)
#         # 关闭数据库连接
#         db.close()
#         print('关闭数据库连接')
#         # 返回微博内容列表contents
#         return contents
#     except Exception as e:
#         print("出错：")
#         db.rollback()
#         print(e)

def saveKeyword(keyword,count):
	 # 连接数据库
    db = pymysql.connect(host="localhost", port=3306,database="sentiment", user="root",password="newpassword", charset='utf8')
    try:
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        print('游标建立成功,准备存储超话关键词及词频')
        # 获取微博内容数据
        sql = "insert into supertopic_keywords(keyword, count) values (%s,%s) on duplicate key update;"%(keyword,count)
        cursor.execute(sql)
        # 关闭数据库连接
        db.close()
        print('关闭数据库连接')
        # 返回微博内容列表contents
    except Exception as e:
        print("存储关键词出错：")
        db.rollback()
        print(e)

def get_words(text_list,stopword_file):
    text = '。'.join(text_list)
    # text = text.encode("gbk","ignore")
    word_counts = {}
    stop = []
    # 停用词表
    with open(stopword_file,'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            lline = line.strip()
            stop.append(lline)
    # 文本分词
    words = jieba.lcut(text,cut_all=False)
    # 计算词频
    for word in words:
        if word not in stop:
            if word not in word_counts:
                word_counts[word] = 1
            else:
                word_counts[word] = word_counts[word] + 1
    # 存储词频字典
    # try:
    #     for item in word_counts:
    #         tmp = item.split(' ',1)
    #         keyword = item[0]
    #         count = item[1]
    #         saveKeyword(keyword, count)
    # except Exception as e:
    #     print(e)
    #     pass
    # print(word_counts)
    return word_counts
    # jieba的提取主题词方法
    # jieba.analyse.set_stop_words(stopword_file)  # file_name为自定义停用词表路径，每行一个词
    # words = list(jieba.analyse.extract_tags(text, topK=7, withWeight=False, allowPOS=()))

#参数word_counts为词频字典，img_file为背景图片文件路径
def generate_img(word_counts, img_file):
    # data = ' '.join(word[0] for word in words)
    # 将图片作为词云背景
    background_image = np.array(Image.open(img_file))
    wc = WordCloud(
        background_color='white',
        mask=background_image,
        font_path='C:\Windows\Fonts\msyh.ttc',
        collocations=False,
        max_words=200,
        min_font_size=5,
        max_font_size=40,
        contour_width=2,
        contour_color ='steelblue',
    )
    wc.generate_from_frequencies(word_counts)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    wc.to_file('./dataset/tp_wordcloud.png')
    print('超话词云图生成完成。')

# if __name__ == '__main__':
def create_supertopic_wordcloud(text_list):
    stopword_file = './dataset/stopword.txt'
    img_file = './dataset/01.png'
    # text_list= getText()
    word_counts = get_words(text_list,stopword_file)
    generate_img(word_counts,img_file)

