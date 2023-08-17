# 从网上读取城市列表信息，并遍历部分城市信息，从API接口中爬取天气信息。
import requests
import re
import time

# 爬取城市信息列表
url = "https://cdn.heweather.com/china-city-list.txt"
res = requests.get(url)
data = res.content.decode('utf-8')

# 使用换行符拆分出每一条城市信息数据
dlist = re.split('[\n\r]+',data)

# 剔除前两条无用的数据
for i in range(2):
    dlist.remove(dlist[0])
# 输出城市信息条数
print(len(dlist))

# 输出前10条信息
for i in range(3,13):
    #使用空白符拆分出每个字段信息
    item = re.split("\s+",dlist[i])
    #输出
    #print(item)
    #print(item[3],":",item[5])
    #爬取指定城市的天气信息
    url = "https://free-api.heweather.com/s6/weather?location=%s&key=25acc7e6d45a47518cb5c0d8e4a254d7"%(item[5])
    res = requests.get(url)
    time.sleep(2)
    #解析json数据
    datalist = res.json()
    data = datalist['HeWeather6'][0]
    #输出部分天气信息
    print("城市：",data['basic']['location'])
    print("今日：",str(data['daily_forecast'][0]['date']))
    print("温度：",data['daily_forecast'][0]['tmp_min'],"~",data['daily_forecast'][0]['tmp_max'])
    print(data['daily_forecast'][0]['cond_txt_d']," . ",data['daily_forecast'][0]['cond_txt_n'])
    print(data['daily_forecast'][0]['wind_dir'],data['daily_forecast'][0]['wind_sc'],'级')
    print("="*70)