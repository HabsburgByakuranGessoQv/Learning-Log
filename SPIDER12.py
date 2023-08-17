# 文件初始化
from pyquery import PyQuery as pq

#windows系统默认使用GBK编码，使用pyquery解析本地html文件，如果文件中有中文则会报错
#UnicodeDecodeError. 'gbk' codec can't decode byte XXX in position XX. illegal multbyte sequence
#不能使用 doc = pq(filename='filepath', encoding='utf-8'); 会报错.
with open("./SX10.html", encoding="utf-8") as f:
       content = f.read()
       f.close()
doc = pq(content)

'''
print(doc('title'))
print(doc('h3'))
print(doc('li'))
print(doc('#hid'))
print(doc('ul li a')) #获取ul中的li中的a
print(doc('a:first')) #获取网页中第一个a 最后：last
print(doc('a:eq(2)')) #获取网页中索引位置为2的a
'''

'''
#获取class属性值为shop的所有节点
print(doc("li.shop"))

#获取超链接
print(doc("a"))
print(doc("a[href*='jd']")) #解析出href中含有‘jd’的超链接
'''

#获取网页中所有ul中li的a节点
alist = doc("ul li a")
#print(type(alist))
for a in alist.items():
       print(a.text(), end=' : ') #a.text() == a.html()
       print(a.attr('href')) #a.attr('href') == a.attr.href


