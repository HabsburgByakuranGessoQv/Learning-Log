#1.导入函数库
from urllib import request
import ssl
import re

#若报错:unable to get local issuer certificate (无法获取本地颁发者证书) 错误
#ssl._create_default_https_context = ssl._create_default_unverified_context #全局取消证书验证

#2.准备请求的url地址，创建请求对象，封装请求参数
url = "https://www.baidu.com" #URL地址
req = request.Request(url)

#3.发送请求，并返回response响应对象
res = request.urlopen(req) #发送请求

#4.解析结果
print(res.status) #输出响应状态码 200
print(res.version) #版本
print(res.reason) # 响应描述字符串 ok
print(res.geturl()) #得到URL码
print(res.getheaders()) #获取响应头信息

#获取响应内容
html = res.read().decode("utf-8")
print(re.findall("<title>(.*?)</title>", html))

#5.储存结果