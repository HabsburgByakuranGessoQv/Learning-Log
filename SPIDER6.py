#requests 爬虫库的使用
import requests
import re

#定义请求信息
url = "http://httpbin.org/post"
data = {'name':'ASRR', 'age':'22'}

#post请求
res = requests.post(url, data=data)

print("status:", res.status_code)
ja = res.json()
print(ja['form']['name'])
print(ja['form']['age'])

print("**********NEXT********")

url = "http://www.baidu.com"
res = requests.get(url)

print("status:", res.status_code)

'''
#res.encoding = "ISO-8859-1" #修改编码
print(res.encoding) #获取编码
print(res.text) #获取响应内容
等于下面这句话
'''
html = res.content.decode("utf-8")
#print(html)

print(re.findall("<title>(.*?)</title>", html))

