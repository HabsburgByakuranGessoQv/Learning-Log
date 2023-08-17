# 批量 创建文件夹

import os #倒入OS模块 创建文件夹 需要的

# 保存路径，直接从电脑文件夹中复制过来，但是

# 注意，直接复制过来的C:\English\LETS\雅思听力 路径结尾是没斜杠的。

# 路径是需要 斜杠结尾的，否则 会以LETS为根目录，而不是“雅思听力”为根目录。

# 但是如果之间加上 斜杠 \ ,你会发现报错。 因为python 中路径结尾必须是 反斜杠，

# 所以直接加个 反斜杠就行了。

path = r'.\demo'

# 定义文件夹名称

name = "Python剑雅"

# 创建10个文件夹，序号为0-9

for i in range(10):

    # "文件"+

    # os.path.exists(path) 判断文件是否存在 固定语法，记住就行

    # 定义一个变量判断文件是否存在,path指代路径,str(i)指代文件夹的名字

    # name+str(i+1)为拼接 名称，效果为：Python剑雅1，Python剑雅2...

    # str(i+1)提高用户体验1，2，3，...
    filename = name + str(i + 1)
    isExists = os.path.exists(os.path.join(path, filename))
    print(os.path.join(path, filename))
    if not isExists:

        # os.path.exists(path+str(i)) 创建文件夹 路径+名称

        os.makedirs(os.path.join(path, filename))

        print("%s 目录创建成功"%i)

    else:

        print("%s 目录纯在" %i)

        # 如果文件不存在,则继续上述操作,直到循环结束

        continue
