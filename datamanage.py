# mysql数据库服务器，端口：3306，而且服务器是处于启动状态
# 安装pymysql：pip install pymysql
import pymysql
import threading
import re
from DBsettings import MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_PWD, MYSQL_USER,MYSQL_CHARSET


class DataManager():
    # 单例模式，确保每次实例化都调用一个对象。
    _instance_lock = threading.Lock()

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(DataManager, "_instance"):
    #         with DataManager._instance_lock:
    #             DataManager._instance = object.__new__(cls)
    #             return DataManager._instance
    #
    #     return DataManager._instance

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PWD, db=MYSQL_DB, charset=MYSQL_CHARSET)
        print("数据库连接成功")

        # 建立游标
        self.cursor = self.conn.cursor()
        print("建立游标成功")

    def create_t_blogs(self):
        sql_create_t_blogs = '''CREATE TABLE IF NOT EXISTS blogs (id BIGINT AUTO_INCREMENT NOT NULL COMMENT 'ID', blog_id VARCHAR(32) COMMENT '微博ID', creator_nickname VARCHAR(64) COMMENT '发贴人昵称', blog_content VARCHAR(1024) COMMENT '微博内容', creator_id VARCHAR(64) COMMENT '发贴人ID', creat_time VARCHAR(128) COMMENT '微博内容创建时间', PRIMARY KEY (id));'''
        self.cursor.execute(sql_create_t_blogs)
        print("创建表成功。")

    def save_data_to_mysql(self, data):
        # 数据库操作

        table = "blogs"
        insert_sql_blogs= '''insert into blogs (blog_id, creator_nickname, blog_content, creator_id, created_time, sentiment_score, sentiment) values(%s,%s,%s,%s,%s,%f,%s)'''
        #
        # (2)准备数据
        # data = ('nancy','30','100','太好笑了')
        # (3)操作
        #repetition = self.cursor.fetchone()

        try:
            print("准备插入数据")
            self.cursor.execute(insert_sql_blogs, data)
            self.conn.commit()
            print('插入成功')
        except Exception as e:
            # 错误时回滚
            print('插入失败，具体见数据库报错')
            self.conn.rollback()  # 回滚
            # if "key 'PRIMARY'" in e.args[1]:
            #     print('数据已存在，未插入数据')
            # else:
            #     print("数据库错误，原因%d: %s"% (e.args[0], e.args[1]))


    def save_fans_to_mysql(self, data):
        # 数据库操作

        table = "supertopic_fans"
        insert_sql_fans= '''insert into supertopic_fans (creator_id, creator_nickname, creator_gender) values(%s,%s,%s)'''
        #
        # (2)准备数据
        # data = ('nancy','30','100','太好笑了')
        # (3)操作
        #repetition = self.cursor.fetchone()

        try:
            print("准备插入超话粉丝数据")
            self.cursor.execute(insert_sql_fans, data)
            self.conn.commit()
            print('插入超话粉丝数据成功')
        except Exception as e:
            # 错误时回滚
            print('插入失败，具体见数据库报错')
            self.conn.rollback()  # 回滚
            if "key 'PRIMARY'" in e.args[1]:
                print('粉丝数据已存在，未插入数据')
            else:
                print("数据库错误，原因%d: %s"% (e.args[0], e.args[1]))

    def is_existed(self, data):
        existed_sql = "select count(blogs.blog_id) from blogs where blog_id = '%s';"%(data)
        try:
            self.cursor.execute(existed_sql)
            res = self.cursor.fetchone()
            if res[0] == 0:
                return 0
            else:
                return 1
        except:
            print("blog_id查询失败"+str(existed_sql))

    def is_creator_existed(self, data):
        existed_sql = "select count(supertopic_fans.creator_id) from supertopic_fans where creator_id = '%s';"%(data)
        try:
            self.cursor.execute(existed_sql)
            res = self.cursor.fetchone()
            if res[0] == 0:
                return 0
            else:
                return 1
        except:
            print("用户id查询失败"+str(existed_sql))

    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
