import jieba
import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import random
import time
import csv
import pandas as pd
import jsonpath

from datamanage import DataManager

# 实例化数据库对象
db = DataManager()

# 判空
def getDataFormList(temp_list):
    if len(temp_list) > 0:
        return temp_list[0].strip()
    else:
        return ''

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'method': 'GET',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhD2inmZvEY9N-ZNkH52FmA5NHD95QcS0qfS02p1h24Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSoMcSKMpeKnp1Btt; SUB=_2A25NS2XoDeRhGeBJ7VcW8S_EyjWIHXVutAugrDV6PUJbktAfLVnykW1NRinJWjp3NXZmmLtKIAOPjHDJB-LZA8fo; SSOLoginState=1615795640; MLOGIN=1; WEIBOCN_FROM=1110103030; _T_WM=93057680546; XSRF-TOKEN=ba3044; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D98%2526q%253D%25E6%258A%2591%25E9%2583%2581%25E7%2597%2587%2526t%253D0%26featurecode%3D10000326%26oid%3D4594832997101078%26fid%3D100808f86f9e10c1d3bdefe430d95f95388c90_-_feed%26uicode%3D10000011',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # 'X-Xsrf-Token': 'a08d05',
}

max_page = 300

def get_page(page, since_id: str):
    params = {
        'extparam': '%E6%8A%91%E9%83%81%E7%97%87',
        'containerid': '100808f86f9e10c1d3bdefe430d95f95388c90',
        'luicode': '10000011',
        # 'page': page,
        'lfid': '100103type%3D98%26q%3D%E6%8A%91%E9%83%81%E7%97%87%26t%3D0',
        'since_id': since_id
    }

    # if page == 1:
    #     url = 'https://m.weibo.cn/api/container/getIndex?extparam=%E6%8A%91%E9%83%81%E7%97%87&containerid=100808f86f9e10c1d3bdefe430d95f95388c90&luicode=10000011&lfid=100103type%3D98%26q%3D%E6%8A%91%E9%83%81%E7%97%87%26t%3D0&since_id=4616556061661064'
    # else:
    url = base_url + urlencode(params)
    # print('page:{},新取的url：{}'%(page,url))
    print(url)
    try:
        response = requests.get(url, headers=headers)
        print(response)
        if response.status_code == 200:
            # response = response.text
            # print(type(response))  # tuple
            return response.json(), page
        else:
            print("请求失败了。")
    except requests.ConnectionError as e:
        print('Error:数据转换失败', e.args)

# def is_existed(blogId):
#     # 之后优化，把blog_id存表，每次校验是否已经存过改成查表
#     # if blogId in keywords:
#     #     return 1
#     # else:
#     #     return 0
#     csv_keyword = csv.reader(open('dataset/data.csv', 'r', encoding='utf-8'))
#     csv_keyword = [row[1] for row in csv_keyword]
#     print(csv_keyword)
#     keywords = []
#     for row in csv_keyword:
#         # print(row)
#         if blogId in keywords:
#             return 1
#         else:
#             keywords.append(row)
#             return 0

def save_to_csv(resource_data):
    file_name = 'dataset/data2.csv'
    # print(type(resource_data))    # tuple
    resource_data = list(resource_data)
    # print(type(resource_data))    # list
    save = pd.DataFrame([resource_data], columns = ['blog_id', 'creator_nickname', 'blog_content', 'creator_id', 'created_time', 'sentiment_score','sentiment'])    # columns=['blog_id','creator_id','creator_nickname', 'blog_content', 'thumbnail_pic','collection_count', 'comment_count', 'repost_count', 'create_time']
    try:
        save.to_csv(file_name, mode='a', header=0, index=0)
        print("写入成功\n")
    except UnicodeEncodeError:
        print("编码错误，数据转换失败，无法写入。")

def get_score(text):
    df = pd.read_table(r"dataset\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
    key = df['key'].values.tolist()
    score = df['score'].values.tolist()
    # jieba分词
    segs = jieba.lcut(text, cut_all=False)  # 返回list
    # 计算得分
    score_list = [score[key.index(x)] for x in segs if (x in key)]
    score = format(sum(score_list), '.4f')
    return score

def get_sentiment(score):
    # nonlocal sentiment = '暂未计算'
    if score > 0.7:
        sentiment = '积极'
    else:
        sentiment = '消极'
    return sentiment

def parse_page(json, page: int):
    # print(type(json))
    # print(json)
    global sentiment
    sentiment = '暂未计算'
    while json:
        try:
            since_id = json.get('data').get('pageInfo').get('since_id')
        # print('parse_page函数内部的打印:'+(page, since_id))
        except:
            print('没有since_id了。回到超话下最新的内容开始获取。')
            since_id = ''
            break

        items = json.get('data').get('cards')   # cards是个列表
        # print(type(items))  # cards是个list
        items = items[0].get('card_group')
        if items == None:
            break
        for index, item in enumerate(items):
            # if page == 1 and index == 1:
            #     continue
            # else:
            if item.get('mblog'):
                item = item.get('mblog',{})
            else:
                continue

            blog = {}

            blog['blog_id'] = item.get('id')
            blog_id = item['id']
            res = db.is_existed(blog_id)
            if res == 1:
                print('------------- 已存过，下一个 -----------\n')
                continue    # 根据blog_id判断，已经存过则跳过解析本条微博

            blog['blog_content'] = pq(item.get('text')).text()
            if blog['blog_content'] != '':
                blog_content = item['text']
                blog['blog_content'] = pq(item.get('text')).text()
            else:
                blog['blog_content'] = "纯图片"

            blog['created_time'] = item.get('created_at')
            created_time = item['created_at']

            user_item = item.get('user', {})    # 获取user字典
            blog['creator_nickname'] = user_item.get('screen_name')
            creator_nickname = user_item['screen_name']

            blog['creator_id'] = user_item.get('id')
            creator_id = user_item['id']

            blog['creator_gender'] = user_item.get('gender')
            creator_gender = user_item['gender']


            fans_data = (blog['creator_id'],blog['creator_nickname'],blog['creator_gender'])

            try:
                score = get_score(blog_content)
                sentiment = get_sentiment(score)
            except:
                sentiment = '计算情感失败'
                pass

            data = (blog['blog_id'], blog['creator_nickname'], blog['blog_content'], blog['creator_id'],
                    blog['created_time'],score,sentiment)  # 是个元组

            print('parse_page函数中的打印data:' + str(data))
            print('parse_page函数中的打印page:'+str(page))
            # 微博内容、微博id、微博创建者昵称 存储到csv
            save_to_csv(data)
            db.save_data_to_mysql(data)

            is_creator_exist = db.is_creator_existed(creator_id)
            if is_creator_exist == 1:
                print('------------- 已存过该用户信息，下一个 -----------\n')
                continue    # 根据blog_id判断，已经存过则跳过解析本条微博
            else:
                db.save_fans_to_mysql(fans_data)

            # 休息间隔再获取下一个item，防止封禁
            # time.sleep(random.uniform(2,4))
        return since_id  # yield表示返回值则表示该函数是个生成器。

if __name__ == '__main__':
    since_id = ''
    # since_id = '4108231562017875'
    # db.create_t_blogs()
    for page in range(1, max_page + 1):
        print('main函数中打印的page:'+str(page))
        print('main函数中打印的since_id:'+str(since_id))
        json = get_page(page, since_id) # 根据获取的since_id请求新的一页
        # print(type(json)) # tuple
        # print(since_id, *json)
        since_id = parse_page(*json)    # 获取下一页的since_id
        time.sleep(random.uniform(4,10))
