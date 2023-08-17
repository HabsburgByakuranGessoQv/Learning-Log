# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import pyaudio
import wave
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import *

BH_old_data = np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
BH_new_data = [[1, 1, 1, 1], [1, 0, 2, 1], [1, 2, 0, 1], [1, 1, 1, 1]]

def mse(target, predict):
    return ((target - predict)**2).mean()

mse_val =  mse(np.array(BH_old_data), np.array(BH_new_data))
print(mse_val)

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
