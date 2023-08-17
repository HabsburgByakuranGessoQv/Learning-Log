#使用beautifulsoup4库解析html
#导入模块
from bs4 import BeautifulSoup

#读取html文件信息（在真实代码中是爬取网页数据）
f = open("./SX10.html", 'r', encoding='utf-8')
content = f.read()
f.close()

#创建解析对象
soup = BeautifulSoup(content, 'lxml')


#第一种：节点选择器解析
#获取ul并从ul中获取所有子节点
blist = soup.ul.children
print(blist)
#遍历
for li in blist:
    #判断必须是li节点
    if li.name == 'li':
        a = li.a
        #输出a标签节点的内容和属性
        print(a.string, ':', a.attrs['href'])
        #print(li)



#第二种：方法解析
#print(soup.find_all('a'))
blist = soup.find_all('li') #获取所有li节点

for li in blist:
    a = li.find("a")
    #print(a.string, ':', a.attrs['href'])
    print(a.get_text, ':', a.attrs['href'])


#第三种： CSS选择器
#获取ul中所有的li节点 #print(soup.select('ul li'))
blist = soup.select('ul li')
for li in blist:
    a = li.select('a')[0] # 获取li中的a节点
    print(a.get_text, ':', a.attrs['href'])
