# 爬取指定小米商品的详情信息
import requests
import re

product_id = '15472'  # 商品id编号
# header头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.mi.com/buy/detail?product_id=%s' % product_id,
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}
# 请求url地址
url = "https://api2.order.mi.com/product/view?product_id=%s&version=2" % product_id

# 提交请求爬取信息
response = requests.get(url,headers=headers)

# 获取响应json数据
data = response.json()

# 输出商品信息
# print(data)
print(data['data']['goods_list'][1]['goods_info'])
goods = data['data']['goods_list'][1]['goods_info']
print("商品名称：",goods['name'])
print("商品价格：",goods['price'])