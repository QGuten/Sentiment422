# coding:utf-8
import jieba
from jieba.analyse import extract_tags


def extract():
	data = "我很 不开心"
	for keyword in extract_tags(data, topK=5, withWeight=False, allowPOS=('v', 'a', 'ag', 'al')):
		print('%s' % keyword)

extract()