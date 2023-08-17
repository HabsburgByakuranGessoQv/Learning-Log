#GET请求爬取数据实战
'''
#使用urllib库
from urllib import request
import re

#准备带有请求的url地址
url = "https://www.apple.com.cn/shop/buy-iphone/iphone-12"

#封装get请求,并执行发送
req = request.Request(url)
res = request.urlopen(req)

#获取响应信息
print(res.status)
html = res.read().decode('utf-8')

#解析结果
pat = '<title>(.*?)</title>'
str = re.findall(pat, html)
print(str)
'''

#使用request库
import requests
import re

#准备请求参数、url地址
#data = {'product_id':'10000214'}
#url = "http://www.mi.com/buy/detail"

url = "https://www.apple.com.cn/shop/buy-iphone/iphone-12-pro"

#执行get请求
res = requests.get(url)#params=data)

#获取响应内容信息
print(res.status_code)
html = res.content.decode('utf-8')

#解析结果
pat = '<title>(.*?)</title>'
str = re.findall(pat, html)
print(str)