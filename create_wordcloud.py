import jieba
import pymysql
from wordcloud import WordCloud
from cv2 import imread

stopword_file='./dataset/stopword.txt'
img_file='./dataset/01.png'
def getText(data):
	 # 连接数据库
    db = pymysql.connect("localhost", "sentiment", "newpassword", "blogs", charset='utf8')
    try:
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 获取微博内容数据
        sql = "select blog_content from blogs where creator_id = '%s';"%(data)
        cursor.execute(sql)
        # 直接通过数据库查询获取的是((1,张三,男),(2,李四,女))这样的元组格式：
        # 每条记录通过元组记录属性值，同时每条记录作为一个元组元素组成查询结果元组
        results = cursor.fetchall()
        # 将微博内容放入contents列表
        contents = []
        for re in results:
        	#只取了text属性值，可直接extend
            contents.extend(re)
        # 关闭数据库连接
        db.close()
        # 返回微博内容列表contents
        return contents
    except Exception as e:
        print("出错：")
        db.rollback()
        print(e)

text = getText()
words = []
for content in text:

    jieba.analyse.set_stop_words(stopword_file) # file_name为自定义停用词表路径，每行一个词
    word=list(jieba.analyse.extract_tags(text, topK=20, withWeight=False, allowPOS=()))

#参数words为关键词列表，img_file为背景图片文件路径
def generate_img(words, img_file):
    data = ' '.join(word[0] for word in words)
    # 将图片作为词云背景
    image_coloring = imread(img_file)
    wc = WordCloud(
        background_color='white',
        mask=image_coloring,
        font_path='C:\Windows\Fonts\msyh.ttc',
        collocations=False,
        max_words=150,
        min_font_size=5,
        max_font_size=40
    )
    wc.generate(data)
    wc.to_file('test.png')

# wordcloud = WordCloud(background_color="pink",width=1000,height=862,margin=3).generate()