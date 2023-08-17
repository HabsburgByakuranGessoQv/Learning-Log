#爬取猫眼电压帮顶栏目中TOP100的所有电影信息，并写入文件
#URL地址：http://maoyan.com/board/4 其中参数offset表示其实条数
#获取信息：{排名，图片，标题，主演，放映时间，评分}
'''
url地址:
    第一页: http://maoyan.com/board/4?offset=0
    第二页：https://maoyan.com/board/4?offset=10
    第三页：https://maoyan.com/board/4?offset=20
    第四页：https://maoyan.com/board/4?offset=30
    第五页：https://maoyan.com/board/4?offset=40
    第六页：https://maoyan.com/board/4?offset=50
    第七页：https://maoyan.com/board/4?offset=60
    第八页：https://maoyan.com/board/4?offset=70
    第九页：https://maoyan.com/board/4?offset=80
    第十页：https://maoyan.com/board/4?offset=90
请求方式：GET
参数： offset = 0-90
返回值： HTML代码
'''

import requests

url = 'http://maoyan.com/board/4?offset=0'

#封装请求头信息
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

res = requests.get(url, headers=headers)
#res.encoding = 'utf-8'

print(res.text)
