#-*- coding:utf-8 -*-
import os
from openpyxl import load_workbook

# 得到数据路径
MainPath = r'D:\StuData\CanopyFinal'
SavePath = MainPath + r'\yellowing_data'
XlxsPath = MainPath + r'\Stander.xlsx'
filename = os.listdir(MainPath)
filename = filename[:-2]

# 获取数据据信息
Stander = open(MainPath + r'\stander.txt')
StanderDataStr = Stander.read()
StanderDataRaw = [i for i in StanderDataStr.split('\n')]
StanderData = []
for i in StanderDataRaw:
    i, _ = i.split('.jpg')
    StanderData.append(i)

# 进行写入xlxs
# wb = load_workbook(XlxsPath)
# ws = wb.active
Data = []
for i in StanderData:
    NumPer, Date = i.split('_')
    # print(NumPer, '\t', Date)
    if '-' in NumPer:
        # 生成数据导入到excel文件中
        Num, Per = NumPer.split('-')
        DataElem = [Num, Per, Date]
        Data.append(DataElem)
        # ws.append(DataElem)
    else:
        DataElem = [NumPer, '0%', Date]
        Data.append(DataElem)
        # ws.append(DataElem)
print(Data)
# wb.save(XlxsPath)
