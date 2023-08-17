#解析库的使用
from lxml import html
etree = html.etree
#准备html文件信息（在真实项目中是从互联网中读取）
f = open("./SX10.html", 'r', encoding='utf-8')
content = f.read()
f.close()

print(content)

#使用lxml创建节点选择器对象
html = etree.HTML(content)

#使用xpath 解析网页中所有元素的节点(标签)
#result = html.xpath("/*") #子节点
#result = html.xpath("//li") #所有ls子节点
result = html.xpath("//*")
for t in result:
    print(t.tag, end=' ')
print()

#解析网页中所有超链接信息
#result = html.xpath("//li")
#result = html.xpath("//li[@class='item-0']") #获取class 属性值为 0 的li子节点
result = html.xpath("//li[contains(@class, 'shop')]") #获取class 属性值含有 shop 的li子节点
#遍历
for t in result:
    #获取当前li节点中的a子节点
    a = t.find('a')
    #输出当前节点的属性与内容
    print(a.text, ':', a.get('href'))