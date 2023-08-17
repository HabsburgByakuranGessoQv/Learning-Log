"""
图片信息爬取
爬取京东指定商品图片信息， 并且存储在当前目录下。
url地址: https://list.jd.com/list.html?cat=9987,653,655
"""

# 导入库
import requests
from pyquery import PyQuery as pq

# 定义请求的url地址
url = "https://list.jd.com/list.html?cat=9987,653,655"
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62 "
}
# print(headers.values())

# 使用request请求爬取指定url信息
res = requests.get(url, headers=headers)
context = res.text
# print(context)

# 使用pyquery创建解析器
doc = pq(context)

# 解析页面中所有商品的图片信息
img_list = doc("img[width='220'][height='220']")

# 遍历并解析图片的url地址信息
img_number = 1
for img_text in img_list.items():
    # print(img_text)
    # 注意.items()步骤为让img_list生成可迭代对象
    # 获取图片的url地址
    img_url = "https:" + str(img_text.attr('data-lazy-img'))
    # img_url = "https:" + str(img_text.attr('src='))
    # print(img_text.attr('data-lazy-img'))
    # # 直接储存图片
    # urlretrieve(img_url, filename='./res/p' + str(img_number) + '.jpg')
    # 存储图片
    with requests.get(img_url, stream=True, headers=headers) as img_on:
        with open("./res/p" + str(img_number) + '.jpg', 'wb') as f:
            for chunk in img_on.iter_content(chunk_size=512):
                f.write(chunk)
            f.close()
    img_number += 1
