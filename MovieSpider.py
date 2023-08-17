import json
import re
import time
import requests
import xlwt


def respone(url):
    # 模拟谷歌浏览器请求头
    headers = {
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
    # 发请求并获取响应
    res = requests.get(url, headers=headers)
    # 将响应的编码格式设置为utf-8
    res.encoding = 'utf-8'
    try:
        # json格式转码
        html = json.loads(res.text)
    except json.decoder.JSONDecodeError:
        # 若不是json格式则直接获取html源码
        html = res.text

    return html


# 正则匹配影片外国名
def re_foreign_name(html):
    name = re.findall(r'<span property="v:itemreviewed">(.+?)</span>', html)[0]
    name = name.split(' ')
    name.pop(0)
    foreign_name = ''
    for ch in name:
        if ch == name[-1]:
            foreign_name += ch
        else:
            foreign_name += (ch + ' ')

    return foreign_name  # 影片外国名


# 正则匹配评价数
def re_evaluation(html):
    evaluation = re.findall(r'property="v:votes">(.+?)</span>', html)[0]

    return evaluation  # 评价数


# 正则匹配概况
def re_introduction(html):
    introduction = re.findall(r'v:summary" class="">(.+?)</span>', html, re.S)[0]
    introduction = introduction.replace(' ', '').replace('\n', '')[2:]

    return introduction  # 概况


# 正则匹配导演
def re_director(html):
    director = re.findall(r'v:directedBy">(.+?)</a>', html, re.S)[0]

    return director  # 导演


# 正则匹配主演
def re_actors(html):
    actors_data = re.findall(r'v:starring">(.+?)</a>', html, re.S)
    actors = ''
    for actor in actors_data:
        if actor == actors_data[-1]:
            actors += actor
        else:
            actors += (actor + ' | ')

    return actors  # 主演


# 正则匹配年份
def re_years(html):
    years_data = re.findall(r'initialReleaseDate" content="(.+?)"', html)
    years = ''
    for year in years_data:
        if year == years_data[-1]:
            years += year
        else:
            years += (year + ' | ')

    return years  # 年份


# 正则匹配地区
def re_region(html):
    region = re.findall(r'\u5236\u7247\u56fd\u5bb6\u002f\u5730\u533a:</span>(.+?)<br/>', html)[0]
    region = region.replace(' ', '')

    return region  # 地区


# 正则匹配类别
def re_types(html):
    types_data = re.findall(r'v:genre">(.+?)</span>', html)
    types = ''
    for Type in types_data:
        if Type == types_data[-1]:
            types += Type
        else:
            types += (Type + ' | ')

    return types  # 类别


# 将匹配到的文件写入文件中
def write_data(movie_datas):
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建写入文件
    worksheet = workbook.add_sheet('movies')  # 创建工作表

    line1 = ['排名', '影片中文名', '评分', '评价数', '导演', '主演', '年份', '地区', '类别']
    for index, col_name in enumerate(line1):
        worksheet.write(0, index, label=col_name)  # 写入第一行

    line = 1
    rates = []  # 存所有评分
    names = []  # 存所有电影名
    urls = []  # 存所有电影详情链接
    evaluations = []  # 存所有的评价数

    for movie_data in movie_datas:
        # 写排名
        worksheet.write(line, 0, label=str(line))
        for index, data in enumerate(movie_data):
            # 写电影所有数据
            worksheet.write(line, index + 1, label=data)
        line += 1  # 每写一行，行数+1

    workbook.save('Douban_movies.xls')  # 保存写入文件


def MovieSpider():
    movie_counts = int(input('\n>>> 请输入你想获取的电影数量：'))
    start = time.time()  # 爬取开始时间
    print('\n>>> 开始爬取...预计耗时：%d 秒\n' % (movie_counts * 2.5))
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8F%AF%E6%92%AD%E6%94%BE&sort=rank&page_limit={}&page_start=0'.format(
        movie_counts)

    movie_datas = []  # 存所有电影信息
    failure = 0  # 失败电影数

    html = respone(url)
    for datas in html["subjects"]:
        try:
            movie_data = [datas['title']]  # 存某电影所有信息
            url = datas['url']
            html = respone(url)
            movie_data.append(datas['rate'])  # 评分
            evaluation = re_evaluation(html)
            movie_data.append(evaluation)  # 评价数
            director = re_director(html)
            movie_data.append(director)  # 导演
            actors = re_actors(html)
            movie_data.append(actors)  # 主演
            years = re_years(html)
            movie_data.append(years)  # 年份
            region = re_region(html)
            movie_data.append(region)  # 地区
            types = re_types(html)
            movie_data.append(types)  # 类别
            movie_datas.append(movie_data)
            print('>>> 链接：%s    电影名称：%s ---> 爬取成功' % (datas['url'], datas['title']))

        except Exception as error:
            print('>>> 链接：%s    电影名称：%s ---> 爬取失败' % (datas['url'], datas['title']))
            print('>>> 失败原因：', error)
            failure += 1

        time.sleep(2)  # 每次爬取睡眠2秒

    end = time.time()  # 爬取结束时间
    times = end - start
    print('\n>>> 全部电影爬取完毕，成功爬取 %d 部，失败 %d 部' % (movie_counts - failure, failure))
    print('    总耗时：%d 秒\n' % times)

    print('>>> 开始将全部爬取的数据写入excel文件中...')
    write_data(movie_datas)
    print('    数据已全部写入excel文件中 ---> Douban_movies1.xls\n')


if __name__ == '__main__':
    MovieSpider()
