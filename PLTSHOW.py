import PIL.Image as image
import matplotlib.pyplot as plt
import numpy as np
import xlrd
from wordcloud import WordCloud

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False


# 从文件中获取数据
def read_data():
    # 打开数据文件
    data = xlrd.open_workbook('Douban_movies.xls')
    table = data.sheets()[0]  # 操作工作表一

    # 获取第5列数据
    directors = table.col_values(4)[1:]
    director_count = {}
    for director in directors:
        # 得key为导演，value为负责的电影数量的字典
        director_count[director] = director_count.get(director, 0) + 1

    actors = table.col_values(5)[1:]
    actor_count = {}
    for actor in actors:
        actor_list = actor.split(' | ')
        for actor in actor_list:
            # 得key为主演，value为参演的电影数量的字典
            actor_count[actor] = actor_count.get(actor, 0) + 1

    years = table.col_values(6)[1:]
    year_count = {}
    for year in years:
        year_list = year.split(' | ')
        # for year in year_list:
        year = year_list[0]
        year = year[:4]
        if int(year) <= 1980:
            year = '1980之前'
        elif 1980 < int(year) <= 1990:
            year = '1981-1990'
        elif 1990 < int(year) <= 2000:
            year = '1991-2000'
        elif 2000 < int(year) <= 2010:
            year = '2001-2010'
        elif 2010 < int(year) <= 2020:
            year = '2011-2020'
        # 得key为年代，value为上映的电影数量的字典
        year_count[year] = year_count.get(year, 0) + 1

    return director_count, actor_count, year_count

# 读取数据
director_count,actor_count,year_count = read_data()

# 生成年代的柱状图
x = np.arange(len(year_count))  # x轴
xdata = []  # x轴说明文字
ydata = []

items = list(year_count.items())
# 按年代由小到大排序
items.sort(key=lambda x: x[0][:4], reverse=False)
# print(items)
# [('1980之前', 26), ('1981-1990', 14), ('1991-2000', 50), ('2001-2010', 75), ('2011-2020', 84)]

for name, count in items:
    xdata.append(name)
    ydata.append(count)

fig = plt.figure()  # 控制画布大小

# align控制条形柱位置
# color控制条形柱颜色
# label为该条形柱对应图示
# alpha控制条形柱透明度

plt.title('电影上映数年代分布图', fontsize=10)  # 添加标题
plt.xlabel('电影上映年份')
plt.ylabel('电影上映数量')
plt.plot(xdata, ydata, color='red', dash_capstyle='butt')
# plt.show()  # 是否打开图形输出器，如有需要再打开
plt.savefig('电影上映数年代分布图.png')  # 保存为当前目录下的图片
plt.clf()  # 关闭图形编辑器

# -------------------主演图----------------------
x = np.arange(10)  # x轴
xdata = []  # x轴说明文字
ydata = []

items = list(actor_count.items())
items.sort(key=lambda x: x[1], reverse=True)
for name, count in items[:10]:
    xdata.append(name)
    ydata.append(count)

plt.figure(figsize=(14, 10), dpi=100)
plt.title('十大最佳主演', fontsize=10)  # 添加标题
plt.bar(range(len(xdata)), ydata, width=0.3)
plt.xlabel('主演')
plt.ylabel('次数')
plt.xticks(range(len(xdata)), xdata)

# plt.show()  # 是否打开图形输出器，如有需要再打开
plt.savefig('十大最佳主演.png')  # 保存为当前目录下的图片
plt.clf()  # 关闭图形编辑器

# ------------------------导演图---------------------
x = np.arange(10)  # x轴
xdata = []  # x轴说明文字
ydata = []

items = list(director_count.items())
items.sort(key=lambda x: x[1], reverse=True)

for name, count in items[:10]:
    xdata.append(name)
    ydata.append(count)

explo = [0.1, 0.1, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
plt.figure(figsize=(10, 10), dpi=80)
plt.pie(ydata, labels=xdata, explode=explo, shadow=True, startangle=90)
plt.title('十大最佳导演', color='lightblue')
# plt.show()
plt.savefig('十大最佳导演.png')  # 保存为当前目录下的图片
plt.clf()  # 关闭图形编辑器


# -----------------词云图------------------
items = list(actor_count.items())
items.sort(key=lambda x: x[1], reverse=True)

word_list = []
for item in items:
    word_list.append(item[0])

text = " ".join(word_list)

# 打开词云背景图
mask = np.array(image.open("mask1.jpg"))
# 生成词云图
wordcloud = WordCloud(mask=mask, font_path="C:\\Windows\\Fonts\\msyh.ttc", background_color='white').generate(text)
# 保存词云图
wordcloud.to_file("词云.jpg")
