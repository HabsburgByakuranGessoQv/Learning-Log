#post爬取数据实战
#使用requests发送post数据，并抓取有道翻译的信息
'''
分析有道翻译信息爬取方案:
    url地址:https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule
    请求方式:post
    参数: i: red   doctype: json
    响应结果: application/json; charset=utf-8; json格式数据
'''

'''
#不完整url地址
import requests
import json

def fanyi(keyword):
    url = "https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    data = {
        'i':keyword,
        'doctype':'json'
    }

    #发送请求
    res =requests.post(url, data=data)

    #判断
    if res.status_code == 200:
        #获取结果
        json_data = res.content.decode('utf-8')
        #未解析json的内容以及格式
        #print(type(json_data))
        #print(json_data)

        #json转化
        #print(type(json.loads(json_data))) #查看json 格式
        #json_data_fin = json.loads(res.content.decode('utf-8'))
        json_data_fin = res.json()
        #print(json_data_fin) #内容/json
        print(keyword, ':', json_data_fin['translateResult'][0][0]['tgt'])
    else:
        print("ERROE:网络请求失败(!=200)")

#主入口程序判断
if __name__ == '__main__':#循环
    while True:
        keyword = input('请输入您要翻译的信息:')
        if keyword == 'exit()':#退出
            break
        fanyi(keyword) 
'''

#完整url地址
import requests
import time, random, hashlib

#*************************************************************#
# 生成data中salt和sign两个数据
def salt_sign(keyword):
    # m = hashlib.md5()
    now_time = int(time.time() * 1000)
    salt = now_time + random.randint(1, 10)
    sign = "fanyideskweb" + keyword + str(salt) + "n%A-rKaT5fb[Gy?;N5@Tj"
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
    return (salt, sign, now_time)
#*************************************************************#

def fanyi(keyword):
    #调用生成签名函数,负责获取所需信息
    salt, sign, now_time = salt_sign(keyword)

    url = "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    #data提交制定
    data = {
        'i':keyword,
        'from':'AUTO',
        'to':'AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'salt':salt,
        'sign':sign,
        #ts bv 不需提交
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }

    #封装浏览器头信息 根据不同网站的需求来进行筛选上报
    headers = {
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-1578341664@10.108.160.101; JSESSIONID=aaajxOzuoYxJG5j9CPESx; OUTFOX_SEARCH_USER_ID_NCOO=1242880105.851873; ___rl__test__cookies='+str(now_time),
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'
    }

    #发送请求
    res =requests.post(url, data=data, headers=headers)

    #判断
    if res.status_code == 200:
        #获取结果
        json_data = res.content.decode('utf-8')
        #未解析json的内容以及格式
        #print(type(json_data))
        #print(json_data)

        #json转化
        #print(type(json.loads(json_data))) #查看json 格式
        #json_data_fin = json.loads(res.content.decode('utf-8'))
        json_data_fin = res.json()
        #print(json_data_fin) #内容/json
        print(keyword, ':', json_data_fin['translateResult'][0][0]['tgt'])
    else:
        print("ERROE:网络请求失败(!=200)")

#主入口程序判断
if __name__ == '__main__':#循环
    while True:
        keyword = input('请输入您要翻译的信息:')
        if keyword == 'exit()':#退出
            break
        fanyi(keyword)
