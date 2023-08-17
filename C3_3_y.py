# -*- coding: utf-8 -*-
from speechlib import *

(framerate, wave_data) = wavfile.read("C3_3_y.wav")  # 读取数据

# 参数设置
wlen = 256
nfft = wlen
# win = np.hanning(wlen)
inc = 128
# 画语谱图
plt.specgram(wave_data, nfft, framerate, noverlap=inc, cmap='jet')
plt.xlabel("时间/s")
plt.ylabel("频率/Hz")
plt.title("语谱图")
plt.show()
