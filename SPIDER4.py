from urllib import request
import ssl
import re

#封装request请求
url = "http://news.baidu.com/"
req = request.Request(url)

#执行请求获取响应信息
res = request.urlopen(req)

#获取响应内容
con = res.read().decode("utf-8")

#使用正则解析结果
pat = '<a href="(.*?)" mon=".*?" target="_blank">(.*?)<span class="related-video-icon"></span></a>'
dlist = re.findall(pat, con)

#遍历输出结果
for v in dlist:
    if v[1] != '#{title}':
        print(v[1]+":"+v[0])