import pymysql
import pandas as pd
import jieba

def get_conn():
    conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='newpassword',database='sentiment',charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn,cursor

def cul_sentiment(content,avrscore):
    ''' 计算情感值及情感偏向 '''
    df = pd.read_table(r"dataset\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
    key = df['key'].values.tolist()
    score = df['score'].values.tolist()
    # jieba分词
    segs = jieba.lcut(content, cut_all=False)  # 返回list
    # 计算得分
    score_list = [score[key.index(x)] for x in segs if (x in key)]
    score = sum(score_list)
    if score > 30:
        sentiment = '积极'
    else:
        sentiment = '消极'
    return score, sentiment

def update_sentiment(sql,args):
    sql = "update blogs set sentiment_score = %s where id=%s;"
    result = cur.exec(sql,args)
    conn.commit()
    cur.close()
    conn.close()

def close_conn(conn, cursor):
    cursor.close()
    conn.close()