# 2021.12 学生成绩管理系统 数据结构实验课课程设计
`水平有限，如有错误请指教！相互学习讨论`
### 设计要求原文
>**基本要求**：  
（1）能按学期、按班级完成对学生成绩的录入。  
（2）能按班级统计学生的成绩，求学生的总分及平均分，并采用两种排序算法对学生的平均成绩进行排序  
（3）采用查询方式实现查询学生成绩，不及格科目及学生名单  
（4）能按班级输出学生的成绩单  
（5）能按学号删除学生纪录，成绩等。  
（6）将学生的学号、姓名及各门课程的成绩等信息保存于外部存储器的文件中。  
**创新要求**:  
在基本要求达到后，可进行创新设计，增加新的功能比如班级总排名，单科成绩排名，各分数段学生统计等。使用多种方法排序和查询者，加分！  
**信息描述**：  
>选择一种数据结构（数组，队列，链表等），记录学生成绩信息（包括学生学号、姓名、各门课程的成绩等）。  

[课程设计报告文档](https://github.com/HabsburgGQv/Learning-Log/blob/2760fc04f47ee4dac7f1c46d7a5c54bd8f5c6294/2021.12/%E5%AD%A6%E7%94%9F%E6%88%90%E7%BB%A9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F/%E8%AF%BE%E7%A8%8B%E8%AE%BE%E8%AE%A1%E6%8A%A5%E5%91%8A.pdf)
### 报告中的摘要
本次课程设计我的选题是选题 1：学生成绩管理系统，首先可以完成基本要求的所有
功能（如成绩的录入、按班级统计学生成绩、求总分以及平均分、平均分排序，查询成
绩、输出成绩单、按学号删除、存储信息……）。且经过大量测试、改进、优化后程序 bug
出现概率几乎为 0。创新性功能也十分多样，如班级排名，年级排名，单科排名，分数段
统计……在查询上，学号和姓名任意输入查询，而且非常快速，排序方法上也十分多样，
体现在不同科目或总分排序运用了不同的排序方法，包括希尔排序、快速排序、选择排
序、折半排序、插入排序以及冒泡排序。在数据结构上采用独特的链表式存储，添加操
作有前插和尾插两种，对内存管理十分优秀，解析外部文件、链表信息的程序也十分稳
定，程序的最开始就能迅速地将 json 文件中的数据进行解析，存入临时链表中。其中代
码结构有条理，逻辑性，整篇代码 0 警告，运用 2 大类，多达 28 个函数 746 行代码，有
的函数调用其他函数，代码规范，同时运用 python 第三方包 collections 和 json，在存储
上的不论是观赏性或是解析难度都很优秀，同时学生成绩中，不同科目或其学生属性值
的合法性也可以得到保证，所以作者程序稳定性相较于其他管理系统有充足的信心，函
数间有相应的注释，可读性强，且程序在进行中有相应输出指导用户使用，信息量足。
链表看似引用复杂，但作者结合列表，类列表，字典，类字典对排序、查询、存储操作
便可以顺利实现。
  
### 流程图
![avatar](https://github.com/HabsburgGQv/Learning-Log/blob/a20450aff0da01824432f8a2b840a1d0fc623f24/2021.12/%E5%AD%A6%E7%94%9F%E6%88%90%E7%BB%A9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F/flow_chart.png)
  
### LOGPART
主要还是分为三部分: 指针元素类部分、链表及其操作部分、操作主函数部分。  
gui操作界面是我最开始就想做的但是在过程中没有加入这个模块导致最后不方便做gui，小小的遗憾。  
这个老师的评分重点令人困惑，我这个系统的稳定性很好，没有bug出现，在算法上用了6个排序，和链表结构，但老师问我有什么查询方法的时候我有点无语，都用链表了怎么用特别的查询算法，老师在评分的时候感觉还是比较随意的。。。说到新的功能的时候，难道非要搞个在文件上加密什么之类的功能才“很加分”？本人对分数不是怎么看重，但是规则是最开始写好的，在学生管理的层面的新功能才能叫“加分”吧，我已经写把能加入的功能都已经加入了，稳定性可以说是第一的，但是最后的结果则是测试都没有测试过几次、调试都没有调试过几次的人多分？小小的质疑。。  
不管如何，都已经过去，我已不会再去纠结于此 :)  

### 代码
[源码链接](https://github.com/HabsburgGQv/Learning-Log/blob/a8254f316d80034bc8f462620d6fad9b1a90823e/2021.12/%E5%AD%A6%E7%94%9F%E6%88%90%E7%BB%A9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F/main.py)
```python3
"""
信息: 学期, 班级, 学号, 姓名, 单科(A, B, C), 总分以及平均分(计算)
附加信息: 排序后的班级总排名, 单科排名, 分数段统计
函数: 录入, 班级平均分, 查询不及格名单, 输出, 删除, 存储
附加: 总排名, 单科排名, 分数段统计, 修改成绩函数
"""
from collections import defaultdict
import json


# 指针元素类
class itemNode(object):
    # 初始化 学期, 班级, 学号信息
    def __init__(self, Term, Class, Number):
        self.Term = Term
        self.Class = Class
        self.Number = Number
        self.Name = None
        self.A = 0
        self.B = 0
        self.C = 0
        self.Total = 0
        self.Aver = 0
        self.Rank = 0
        self.RankA = 0
        self.RankB = 0
        self.RankC = 0
        self.next = None

    # 输入操作
    def TypeIn(self):
        Name = input("输入姓名: ")
        self.Name = Name
        try:
            Ag = int(input("输入A成绩: "))
        except ValueError:
            Ag = int(input("请输入正确格式的A成绩: "))
        try:
            Bg = int(input("输入B成绩: "))
        except ValueError:
            Bg = int(input("请输入正确格式的B成绩: "))
        try:
            Cg = int(input("输入C成绩: "))
        except ValueError:
            Cg = int(input("请输入正确格式的C成绩: "))
        self.A = Ag
        self.B = Bg
        self.C = Cg
        self.Total = Ag + Bg + Cg
        self.Aver = int((Ag + Bg + Cg) / 3)

    # 修改
    def Amend(self):
        print("操作\t\t项目\nname\t姓名\nnum\t\t学号\nclass\t班级\nterm\t学期\nA\t\tA\nB\t\tB\nC\t\tC")
        which = input("您想要修改什么？: ")
        if which.isalpha():
            if which == 'name':
                Namenew = input("姓名输入: ")
                self.Name = Namenew
            elif which == 'num':
                Numnew = input("学号输入: ")
                self.Number = Numnew
            elif which == 'class':
                Classnew = input("班级输入: ")
                self.Class = Classnew
            elif which == 'term':
                Termnew = input("学期输入: ")
                self.Term = Termnew
            elif which == 'A':
                try:
                    Anew = int(input("成绩输入: "))
                except ValueError:
                    Anew = int(input("请输入合法成绩: "))
                self.A = Anew
            elif which == 'B':
                try:
                    Bnew = int(input("成绩输入: "))
                except ValueError:
                    Bnew = int(input("请输入合法成绩: "))
                self.B = Bnew
            elif which == 'C':
                try:
                    Cnew = int(input("成绩输入: "))
                except ValueError:
                    Cnew = int(input("请输入合法成绩: "))
                self.C = Cnew
            else:
                print("您输入的操作科目不存在")
        else:
            print("您输入的操作科目不存在")
        self.Total = self.A + self.B + self.C
        self.Aver = int(self.Total / 3)

    # 输出操作
    def Check(self):
        print("姓名： {}".format(self.Name))
        print("学号：{}".format(self.Number))
        print("班级：{}".format(self.Class))
        print("学期：{}".format(self.Term))
        print("A成绩：{}".format(self.A))
        print("B成绩：{}".format(self.B))
        print("C成绩：{}".format(self.C))
        print("总成绩：{}".format(self.Total))
        print("平均分：{}".format(self.Aver))


# 链表类及其操作
class LinkList(object):
    # 链表
    def __init__(self):
        # 初始化链表大小, 而不是创建
        self.head = None  # 首地址指针为None

    # 判断空链表
    def Empty(self):
        return self.head is None

    # 解析先前的数据 加入链表
    def Analysis(self):
        try:
            with open('record.json', 'r', encoding='utf-8') as ExJsonFile:
                ExAll = json.load(ExJsonFile)
                ExJsonFile.close()
            for ExData in ExAll.values():
                # ExAll.values() : dict_values([[{}]])
                # ExData : [{}]
                for ExDict in ExData:
                    # ExDict : {}
                    ExElemDataList = []
                    for ExElemData in ExDict.values():
                        # ExElemData : 所有属性数据 value
                        ExElemDataList.append(ExElemData)
                    TempTerm = ExElemDataList[0]
                    TempClass = ExElemDataList[1]
                    TempName = ExElemDataList[2]
                    TempNum = ExElemDataList[3]
                    TempA = ExElemDataList[4]
                    TempB = ExElemDataList[5]
                    TempC = ExElemDataList[6]
                    TempNode = itemNode(TempTerm, TempClass, TempNum)
                    TempNode.Name = TempName
                    TempNode.A = TempA
                    TempNode.B = TempB
                    TempNode.C = TempC
                    TempNode.Total = TempA + TempB + TempC
                    TempNode.Aver = int(TempNode.Total / 3)
                    TempNode.next = self.head
                    self.head = TempNode
        except json.decoder.JSONDecodeError:
            return

    # 遍历
    def Item(self):
        cursor = self.head
        ElemDict = defaultdict(list)
        while cursor is not None:
            Elem = {
                '学期': cursor.Term,
                '班级': cursor.Class,
                '姓名': cursor.Name,
                '学号': cursor.Number,
                'A': cursor.A,
                'B': cursor.B,
                'C': cursor.C,
                '平均分': cursor.Aver,
                '总分': cursor.Total
            }
            ElemDict["成绩"].append(Elem)
            cursor = cursor.next
        return ElemDict

    # 表格形式显示
    # noinspection PyMethodMayBeStatic
    def PrintItem(self, ElemDict):
        Header = ['学期', '班级', '姓名', '学号', 'A', 'B', 'C', '平均', '总分']
        print('序号', end='\t' * 2)
        for HeaderElem in Header:
            print(HeaderElem, end='\t' * 3)
        print()
        # ElemDict : defaultdict(<class 'list'>, {})
        for i in ElemDict.values():
            # ElemDict.values() : dict_values([[{}]])
            Rank = 1
            for j in i:
                print(Rank, end='\t' * 2)
                Rank += 1
                # i : [{}]    j : {}
                for k in j.values():
                    # k : values()
                    print(k, end='\t' * 3)
                print()

    # 头部添加元素
    def Add(self, ATerm, AClass, ANumber):
        cursor = self.search(ANumber)
        if cursor == 0:
            NewNode = itemNode(ATerm, AClass, ANumber)
            NewNode.TypeIn()
            # 前插法
            NewNode.next = self.head
            self.head = NewNode
            NewNode.Check()
        else:
            cursor.Check()
            print("该学号学生已经存在")

    # 尾部添加元素
    def Append(self, ATerm, AClass, ANumber):
        NewNode = itemNode(ATerm, AClass, ANumber)
        NewNode.TypeIn()
        if self.Empty():
            self.head = NewNode
        else:
            cursor = self.head
            while cursor.next is not None:
                cursor = cursor.next
            cursor.next = NewNode

    # 删除元素
    def Del(self, DIndex):
        cursor = self.head
        tem = None
        # 寻找
        while cursor is not None:
            if cursor.Name == DIndex or str(cursor.Number) == str(DIndex):
                # 如果第一个就是删除的节点
                if not tem:
                    # 头指针指向头指针的后一个节点
                    self.head = cursor.next
                else:
                    # 删除位置前一个指向其删除节点的next
                    tem.next = cursor.next
                cursor.Check()
                return "OK"
            else:
                # 后移节点
                tem = cursor
                cursor = cursor.next
        return "未找到对应学生"

    # 提取数据 并快速排序班级内学生总分 计算班级平均分
    def Extract(self, EClass):
        cursor = self.head
        NumList = []
        TotalList = []
        while cursor is not None:
            if EClass == cursor.Class:
                Number = cursor.Number
                Total = cursor.Total
                NumList.append(Number)
                TotalList.append(Total)
            cursor = cursor.next
        if not TotalList:
            return 0, 0
        Dict = dict(zip(NumList, TotalList))
        key = [value for value in Dict.values()]
        try:
            ClassAver = int(sum(key) / (len(key)))
        except ZeroDivisionError:
            return [], 0
        Quicksort(key, 0, len(key) - 1)
        key.reverse()
        ElemDict = defaultdict(list)
        for i in key:
            RankElem = [key for key, value in Dict.items() if value == i]
            RankNum = RankElem[0]
            RankPeople = self.search(RankNum)
            Elem = {
                '学期': RankPeople.Term,
                '班级': RankPeople.Class,
                '姓名': RankPeople.Name,
                '学号': RankPeople.Number,
                'A': RankPeople.A,
                'B': RankPeople.B,
                'C': RankPeople.C,
                '平均分': RankPeople.Aver,
                '总分': RankPeople.Total
            }
            ElemDict["成绩"].append(Elem)
        return ClassAver, ElemDict

    # 提取数据 并希尔排序 计算平均分 (所有人)
    def ExtractAll(self):
        cursor = self.head
        if cursor is None:
            return [], 0
        NumList = []
        TotalList = []
        while cursor is not None:
            Num = cursor.Number
            Total = cursor.Total
            NumList.append(Num)
            TotalList.append(Total)
            cursor = cursor.next
        Dict = dict(zip(NumList, TotalList))
        key = [value for value in Dict.values()]
        ClassAver = int(sum(key) / (len(key)))
        ShellSort(key)
        key.reverse()
        ElemDict = defaultdict(list)
        for i in key:
            RankElem = [key for key, value in Dict.items() if value == i]
            RankNum = RankElem[0]
            RankPeople = self.search(RankNum)
            Elem = {
                '学期': RankPeople.Term,
                '班级': RankPeople.Class,
                '姓名': RankPeople.Name,
                '学号': RankPeople.Number,
                'A': RankPeople.A,
                'B': RankPeople.B,
                'C': RankPeople.C,
                '平均分': RankPeople.Aver,
                '总分': RankPeople.Total
            }
            ElemDict["成绩"].append(Elem)
        return ClassAver, ElemDict

    # 提取数据 快速排序进行班级平均分排序
    def ExtractClass(self):
        ClassList = []
        GradeAver = {}
        cursor = self.head
        while cursor is not None:
            ClassElem = cursor.Class
            if ClassElem not in ClassList:
                ClassList.append(ClassElem)
            cursor = cursor.next
        for i in ClassList:
            AverElem, _ = self.Extract(i)
            iElem = {i: AverElem}
            GradeAver.update(iElem)
        key = [value for value in GradeAver.values()]
        Quicksort(key, 0, len(key) - 1)
        key.reverse()
        res = []
        for j in key:
            RankElem = [key for key, value in GradeAver.items() if value == j]
            RankElem.append(j)
            res.append(RankElem)
        for Rank in range(len(res)):
            res[Rank].append(Rank + 1)
            res[Rank].reverse()
        return res

    # 提取数据 并冒泡排序(年级单科A)
    def ASort(self):
        cursor = self.head
        NameList = []
        TotalList = []
        while cursor is not None:
            Name = cursor.Name
            ATem = cursor.A
            NameList.append(Name)
            TotalList.append(ATem)
            cursor = cursor.next
        Dict = dict(zip(NameList, TotalList))
        key = [value for value in Dict.values()]
        key = Maopao(key)
        key.reverse()
        res = []
        for i in key:
            RankElem = [key for key, value in Dict.items() if value == i]
            RankElem.append(i)
            res.append(RankElem)
        for Rank in range(len(res)):
            res[Rank].append(Rank + 1)
            res[Rank].reverse()
        return res

    # 提取数据 并选择排序(年级单科B)
    def BSort(self):
        cursor = self.head
        NameList = []
        TotalList = []
        while cursor is not None:
            Name = cursor.Name
            BTem = cursor.B
            NameList.append(Name)
            TotalList.append(BTem)
            cursor = cursor.next
        Dict = dict(zip(NameList, TotalList))
        key = [value for value in Dict.values()]
        key = SelectSort(key)
        key.reverse()
        res = []
        for i in key:
            RankElem = [key for key, value in Dict.items() if value == i]
            RankElem.append(i)
            res.append(RankElem)
        for Rank in range(len(res)):
            res[Rank].append(Rank + 1)
            res[Rank].reverse()
        return res

    # 提取数据 并插入排序(年级单科C)
    def CSort(self):
        cursor = self.head
        NameList = []
        TotalList = []
        while cursor is not None:
            Name = cursor.Name
            CTem = cursor.C
            NameList.append(Name)
            TotalList.append(CTem)
            cursor = cursor.next
        Dict = dict(zip(NameList, TotalList))
        key = [value for value in Dict.values()]
        key = InsertSort(key)
        key.reverse()
        res = []
        for i in key:
            RankElem = [key for key, value in Dict.items() if value == i]
            RankElem.append(i)
            res.append(RankElem)
        for Rank in range(len(res)):
            res[Rank].append(Rank + 1)
            res[Rank].reverse()
        return res

    # 写入操作
    def WriteIn(self):
        resDict = self.Item()
        with open('record.json', 'w', encoding='utf-8', newline='\n') as JsonFile:
            JsonStr = json.dumps(resDict, indent=4, ensure_ascii=False)
            print(JsonStr)
            JsonFile.write(JsonStr)
            JsonFile.close()
        return "成绩写入成功"

    # 不及格名单
    def Fail(self):
        cursor = self.head
        FailList = []
        FailA = []
        FailB = []
        FailC = []
        while cursor is not None:
            if cursor.A < 60:
                FailList.append(cursor.Name)
                FailA.append(cursor.Name)
            elif cursor.B < 60:
                FailB.append(cursor.Name)
                FailList.append(cursor.Name)
            elif cursor.C < 60:
                FailList.append(cursor.Name)
                FailC.append(cursor.Name)
            cursor = cursor.next
        return FailList, FailA, FailB, FailC

    # 统计分数段
    def Sat(self, subject):
        cursor = self.head
        Great = 0
        Good = 0
        Failed = 0
        if subject == 'A':
            while cursor is not None:
                if cursor.A >= 90:
                    Great += 1
                elif cursor.A >= 60:
                    Good += 1
                else:
                    Failed += 1
                cursor = cursor.next
        elif subject == 'B':
            while cursor is not None:
                if cursor.B >= 90:
                    Great += 1
                elif cursor.B >= 60:
                    Good += 1
                else:
                    Failed += 1
                cursor = cursor.next
        elif subject == 'C':
            while cursor is not None:
                if cursor.C >= 90:
                    Great += 1
                elif cursor.C >= 60:
                    Good += 1
                else:
                    Failed += 1
                cursor = cursor.next
        else:
            return "ERROR SUBJECT"
        res = {
            '优秀': Great,
            '良好': Good,
            '不及格': Failed
        }
        return res

    # 查找学生
    def search(self, sIndex):
        cursor = self.head
        while cursor is not None:
            if str(cursor.Name) == str(sIndex) or str(cursor.Number) == str(sIndex):
                return cursor
            cursor = cursor.next
        # print("ERROR" * 100)
        return 0


# 快速排序函数
def Quicksort(qList, start, end):
    if start >= end:  # 递归的退出条件
        return
    mid = qList[start]  # 设定起始的基准元素
    low = start  # low为序列左边在开始位置的由左向右移动的游标
    high = end  # high为序列右边末尾位置的由右向左移动的游标
    while low < high:
        # 如果low与high未重合，high(右边)指向的元素大于等于基准元素，则high向左移动
        while low < high and qList[high] >= mid:
            high -= 1
        qList[low] = qList[high]  # 走到此位置时high指向一个比基准元素小的元素,将high指向的元素放到low的位置上,此时high指向的位置空着,接下来移动low找到符合条件的元素放在此处
        # 如果low与high未重合，low指向的元素比基准元素小，则low向右移动
        while low < high and qList[low] < mid:
            low += 1
        qList[high] = qList[low]  # 此时low指向一个比基准元素大的元素,将low指向的元素放到high空着的位置上,此时low指向的位置空着,之后进行下一次循环,将high找到符合条件的元素填到此处

    # 退出循环后，low与high重合，此时所指位置为基准元素的正确位置,左边的元素都比基准元素小,右边的元素都比基准元素大
    qList[low] = mid  # 将基准元素放到该位置,
    # 对基准元素左边的子序列进行快速排序
    Quicksort(qList, start, low - 1)  # start :0  low -1 原基准元素靠左边一位
    # 对基准元素右边的子序列进行快速排序
    Quicksort(qList, low + 1, end)  # low+1 : 原基准元素靠右一位  end: 最后


# 折半查找函数
def Zheban(arr, start, end, data):
    while start <= end:
        half = int((start + end) / 2)
        if arr[half] == data:
            return half
        elif arr[half] > data:
            end = half - 1
        else:
            start = half + 1
    # 为了防止找不到
    return -1


# 冒泡排序函数
def Maopao(MPList):
    while True:
        flag = 0
        for i in range(len(MPList) - 1):
            if MPList[i] > MPList[i + 1]:
                MPList[i], MPList[i + 1] = MPList[i + 1], MPList[i]
                flag = 1
        if not flag:
            return MPList


# 插入排序函数
def InsertSort(InList):
    resList = [InList[0]]
    for i in InList[1:]:
        flag = 1
        for j in range(len(resList) - 1, -1, -1):
            if i >= resList[j]:
                resList.insert(j + 1, i)
                flag = 0
                break
        if flag:
            resList.insert(0, i)
    return resList


# 希尔排序
def ShellSort(ShList):  # d 为乱序数组，l为初始增量,其中l<len(d),取为len(d)/2比较好操作。最后还是直接省略length输入
    if len(ShList) == (1 or 0):
        return
    length = int(len(ShList) / 2)  # 10
    num = int(len(ShList) / length)  # 2
    while 1:
        for i in range(length):
            ShList_mid = []
            for j in range(num):
                ShList_mid.append(ShList[i + j * length])
            ShList_mid = InsertSort(ShList_mid)
            for j in range(num):
                ShList[i + j * length] = ShList_mid[j]
        length = int(length / 2)
        if length == 0:
            return ShList
        num = int(len(ShList) / length)


# 选择排序
def SelectSort(SeList):
    res = []
    while len(SeList):
        minT = [0, SeList[0]]
        for i in range(len(SeList)):
            if minT[1] > SeList[i]:
                minT = [i, SeList[i]]
        del SeList[minT[0]]  # 找到剩余部分的最小值，并且从原数组中删除
        res.append(minT[1])  # 在新数组中添加
    return res


if __name__ == '__main__':
    StuLink = LinkList()
    StuLink.Analysis()
    while True:
        print("*" * 100)
        print("输入\t操作")
        print("0\tEXIT\n1\t录入\n2\t单科排序/班级排名\n3\t查询\n4\t输出\n5\t删除\n6\t年级总排名/各班级平均分\n7\t写入文件\n8\t修改\n9\t统计分数段\n10\t不及格名单")
        try:
            oper = int(input("请输入您想进行的操作: "))
            print("*" * 43 + "PROGRAM START" + "*" * 44)
            if oper == 1:
                flag1 = 'y'
                while flag1 == 'y':
                    print('*' * 48 + '录入' + '*' * 49)
                    T = input("学期: ")
                    C = input("班级: ")
                    try:
                        N = int(input("学号: "))
                    except ValueError:
                        N = int(input("请输入合法学号: "))
                    StuLink.Add(T, C, N)
                    print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                    flag1 = input("是否继续录入(y/n): ")
            if oper == 2:
                flag2 = 'y'
                while flag2 == 'y':
                    print("A科目 - A\nB科目 - B\nC科目 - C\n班级平均分 班级排名 - S")
                    whichData = input("您想查看什么排序？ ")
                    if whichData == 'A':
                        print("排名\t\t成绩\t\t姓名")
                        for StuElem2 in StuLink.ASort():
                            for value2 in StuElem2:
                                print(value2, end='\t\t')
                            print()
                        print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                    elif whichData == 'B':
                        print("排名\t\t成绩\t\t姓名")
                        for StuElem2 in StuLink.BSort():
                            for value2 in StuElem2:
                                print(value2, end='\t\t')
                            print()
                        print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                    elif whichData == 'C':
                        print("排名\t\t成绩\t\t姓名")
                        for StuElem2 in StuLink.CSort():
                            for value2 in StuElem2:
                                print(value2, end='\t\t')
                            print()
                        print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                    elif whichData == 'S':
                        Class_2 = input("查询哪一个班级？ ")
                        aver2, Dict2 = StuLink.Extract(Class_2)
                        if aver2 == 0:
                            print("不存在该班级")
                            continue
                        print("班级排名:")
                        StuLink.PrintItem(Dict2)
                        print("班级平均分: {}".format(aver2))
                        print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                    else:
                        print("输入功能违法!")
                        print("*" * 43 + "PROGRAM ERROR" + "*" * 44)
                    flag2 = input("是否继续?(y/n) ")
            if oper == 3:
                flag3 = 'y'
                while flag3 == 'y':
                    Cha3 = input("请输入学号或姓名: ")
                    res3 = StuLink.search(Cha3)
                    if res3 != 0:
                        res3.Check()
                    print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                    flag3 = input("是否继续?(y/n) ")
            if oper == 4:
                StuLink.PrintItem(StuLink.Item())
                print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                continue
            if oper == 5:
                flag5 = 'y'
                while flag5 == 'y':
                    Cha3 = input("请输入学号或姓名: ")
                    print(StuLink.Del(Cha3))
                    print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                    flag5 = input("是否继续删除操作?(y/n) ")
            if oper == 6:
                aver6, Dict6 = StuLink.ExtractAll()
                print("年级排名:")
                StuLink.PrintItem(Dict6)
                print("班级平均分排名: {}\n年级平均分: {}".format(StuLink.ExtractClass(), aver6))
                print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                continue
            if oper == 7:
                print(StuLink.WriteIn())
                continue
            if oper == 8:
                flag8 = 'y'
                while flag8 == 'y':
                    oper8 = input("请输入学号或姓名: ")
                    cur8 = StuLink.search(oper8)
                    if cur8 != 0:
                        print("修改前: ")
                        cur8.Check()
                        print("修改:")
                        cur8.Amend()
                        print("修改后:")
                        cur8.Check()
                        print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                    flag8 = input("是否继续?(y/n) ")
            if oper == 9:
                flag9 = 'y'
                while flag9 == 'y':
                    oper9 = input("请输入科目: ")
                    res9 = StuLink.Sat(oper9)
                    print(res9)
                    print("*" * 43 + "PROGRAM FINISH" + "*" * 43)
                    flag9 = input("是否继续?(y/n) ")
            if oper == 10:
                FailAll, FailA10, FailB10, FailC10 = StuLink.Fail()
                print("所有不及格名单： ")
                for All in FailAll:
                    print(All, end='\t')
                print()
                print("A不及格名单： ")
                for All in FailA10:
                    print(All, end='\t')
                print()
                print("B不及格名单： ")
                for All in FailB10:
                    print(All, end='\t')
                print()
                print("C不及格名单： ")
                for All in FailC10:
                    print(All, end='\t')
                print()
                continue
            if oper == 0:
                print("EXITING......")
                print('*' * 42 + 'EXIT THE PROGRAM' + '*' * 42)
                break
            else:
                print("*" * 43 + "ERROR OPERATION" + '*' * 42)
        except ValueError:
            print("*" * 43 + "ERROR OPERATION" + '*' * 42)
            continue
```
