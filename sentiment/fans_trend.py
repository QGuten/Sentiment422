# -*- coding: UTF-8 -*-
from datetime import datetime
from matplotlib import pyplot as plt, ticker
from matplotlib.ticker import MultipleLocator


def fans_trend(x,y):
	# xx=['Thu May 04 21:57:49 +0800 2017','Thu May 04 21:56:37 +0800 2017','Fri Feb 16 00:02:22 +0800 2018']
	# y=[-12.758375881981802,57.843209558027496,-15.956667644199804]
	# x = []
	# for i in xx:
	# 	print(i, type(i))
	# 	dt = datetime.strptime(i,"%a %b %d %H:%M:%S +0800 %Y")
	# 	print(dt, type(dt))
	# 	x.append(dt)
	plt.figure(figsize=(12, 4))
	# plt.ylim([-100.000000000, 100.000000000])
	plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))
	y_major_locator = MultipleLocator(1.000000)
	plt.tick_params(labelsize=10)  # 刻度字体大小13
	# plt.plot(x, y, color="blue", linestyle="--")  # 为线条设置样式，并且填上标签
	plt.rcParams['font.sans-serif'] = ['SimHei']
	plt.rc("font", family='YouYuan', weight="bold")
	plt.xlabel("时间(年-月)")
	plt.ylabel('情感分值')
	plt.title('个人情感变化折点图')
	plt.scatter(x,y)
	plt.show()
# fans_trend()