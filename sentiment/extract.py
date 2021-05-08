# coding:utf-8
import jieba
from jieba.analyse import textrank


def extract():
	data = "抑郁症 暴饮暴食了一个鸡肉卷一杯九珍一盒鸡米花两块原味鸡一份烤翅半个玉米一盒条一个土豆泥一杯奶茶一分多芒小丸子一个提拉米苏杯 想吐 吐不出来难受"
	for keyword in textrank(data, topK=1, withWeight=False):
		print('%s' % keyword)

extract()