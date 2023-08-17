import matplotlib.pyplot as plt
import numpy as np
import xlrd

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False


# 读取数据
data = xlrd.open_workbook('Douban_movies.xls')
table = data.sheets()[0]  # 操作工作表一

# 对地区进行计数
zones = table.col_values(7)[1:]
zone_count = {}

# 对地区进行统计
for zone in zones:
    if '/' in zone:
        # 地区可以有多个 需要进行分割计数
        zone_list = zone.split('/')
        for single_zone in zone_list:
            # key 是 地区， value 是 计数. 每有一次出现， 则 + 1
            zone_count[single_zone] = zone_count.get(single_zone, 0) + 1
    else:
        zone_count[zone] = zone_count.get(zone, 0) + 1

# 可视化 地区 与 数量
items = list(zone_count.items())
# 按数量排序
items.sort(key=lambda x: x[1], reverse=False)
# print(items)

x = np.arange(len(zone_count))  # x轴
xdata = []  # x轴说明文字
ydata = []

for zone_name, count in items:
    xdata.append(zone_name)
    ydata.append(count)

fig = plt.figure(dpi=1000)

plt.title('地区上映数分布图', fontsize=10)
plt.xlabel('地区名称')
plt.ylabel('上映次数')
plt.xticks(rotation=45, fontsize=5)
plt.bar(xdata, ydata)

# plt.show()
plt.savefig('地区上映数量图.png')  # 保存为当前目录下的图片

# Top10
limit = np.arange(10)
xdata = []  # x轴说明文字
ydata = []

items = list(zone_count.items())
items.sort(key=lambda x: x[1], reverse=True)

for zone_name, count in items[:10]:
    xdata.append(zone_name)
    ydata.append(count)

fig = plt.figure(figsize=(10, 10), dpi=600)
plt.title('Top10地区上映数分布图', fontsize=10)
plt.xlabel('地区名称')
plt.ylabel('上映次数')
plt.xticks(rotation=45)
plt.bar(xdata, ydata)

# plt.show()
plt.savefig('十大地区上映数量图.png')  # 保存为当前目录下的图片

# 对类型进行计数
kinds = table.col_values(8)[1:]
kind_count = {}

# 对类型进行统计
for kind in kinds:
    if '|' in kind:
        # 类型可以有多个 需要进行分割计数
        kind_list = kind.split('|')
        for single_kind in kind_list:
            # key 是 类型， value 是 计数. 每有一次出现， 则 + 1
            kind_count[single_kind] = kind_count.get(single_kind, 0) + 1
    else:
        kind_count[kind] = zone_count.get(kind, 0) + 1

# 可视化 类型 与 数量
items = list(kind_count.items())
# 按数量排序
items.sort(key=lambda x: x[1], reverse=False)
# print(items)

x = np.arange(len(kind_count))  # x轴
xdata = []  # x轴说明文字
ydata = []

for kind_name, count in items:
    xdata.append(kind_name)
    ydata.append(count)

fig = plt.figure(dpi=1000)
explo = [0.03 for x in range(len(items))]

plt.title('电影类型数量柱状图', fontsize=10)
plt.xlabel('类型名称')
plt.ylabel('次数')
plt.xticks(rotation=45, fontsize=5)
plt.bar(xdata, ydata)

# plt.show()
plt.savefig('电影类型数量柱状图.png')  # 保存为当前目录下的图片

# Top15
limit = np.arange(10)
xdata = []  # x轴说明文字
ydata = []

items = list(kind_count.items())
items.sort(key=lambda x: x[1], reverse=True)

for kind_name, count in items[:15]:
    xdata.append(kind_name)
    ydata.append(count)

fig = plt.figure()

plt.title('Top15电影类型数量柱状图', fontsize=10)
plt.xlabel('地区名称')
plt.ylabel('次数')
plt.xticks(rotation=45)
plt.bar(xdata, ydata)

# plt.show()
plt.savefig('Top15电影类型数量柱状图.png')  # 保存为当前目录下的图片


# 十大评论最多数量电影排名
# 数据读取
comments = table.col_values(3)[1:]
for i in range(len(comments)):
    comments[i] = float(comments[i])
names = table.col_values(1)[1:]
items = zip(names, comments)
items = dict(items)

items = list(items.items())
items.sort(key=lambda x: x[1], reverse=True)
xdata = []  # x轴说明文字
ydata = []

for name, count in items[:10]:
    xdata.append(name)
    ydata.append(count)

fig = plt.figure(figsize=(10, 10), dpi=600)

plt.title('十大评论最多数量电影排名图', fontsize=10)
plt.xlabel('电影名称')
plt.ylabel('评论次数')
plt.xticks(rotation=45)
plt.bar(xdata, ydata)

plt.savefig('十大评论最多数量电影排名图.png')  # 保存为当前目录下的图片

