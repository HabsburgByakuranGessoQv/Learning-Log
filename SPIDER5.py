from urllib import request
from urllib import error

'''
#URLError 错误处理
url = "http://www.afqwfqg322ew.com/"
req = request.Request(url)

try:
    res = request.urlopen(req)

    html = res.read().decode("utf-8")
    print(len(html))
except error.URLError as e:
    print(e.reason) #输出异常信息


print("ok")
'''

#HTTPError 错误处理
url = "http://img14.360buyimg.com/n0/jfs/t1/193725/1/16798/115477/610bb06bE9f45e7b3/1cd18b0a084edsadasaa1.jpg"
#url = "http://img14.360buyimg.com/n0/jfs/t1/193725/1/16798/115477/610bb06bE9f45e7b3/1cd18b0a084edaa1.jpg"
req = request.Request(url)

try:
    res = request.urlopen(req)
    html = res.read()
    print(len(html))
except error.HTTPError as e:
    print("HTTPERROR\t")
    print(e.reason) #输出异常信息
    print(e.code) #输出状态码信息
#HTTPE 与 URLE 是子父类关系 需要把子类先写到上面
except error.URLError as v:
    print("URLERRE\t")
    print(v.reason)
except:
    print("UNKNOWN ERROR")

print("ok")