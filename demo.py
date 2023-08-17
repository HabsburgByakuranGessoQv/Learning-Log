import os

f = open('test.txt', 'r')
context = f.read()
con_list = context.split('\n')
print(con_list)

import shutil

for filepath in con_list:
    shutil.copy(filepath, r'E:\STUDYCONTENT\Pycharm\torchcon\ImageSets\testfile')
