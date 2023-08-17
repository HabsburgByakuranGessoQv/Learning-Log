# -*- coding: utf-8 -*-
from speechlib import *

(fs, wave_data) = wavfile.read("C3_1_y_1.wav")
t = np.array([i / fs for i in range(wave_data.size)])
sound_max = np.absolute(wave_data).max()
wave_data = wave_data / sound_max
Length = len(wave_data)

wlen = 400
inc = 100

signals = enframe(wave_data, np.hanning(wlen), inc)
# signals = enframe(wave_data,np.hanning(wlen))

i = input("please input first frame number(i):")
tlabel = int(i)
k = int(i)

x = np.arange((tlabel - 1) * inc, (tlabel - 1) * inc + wlen)
y = signals[tlabel, :]
# plt.figure(figsize=(4,3))
plt.figure(1)
plt.subplot(411)
plt.plot(x, y, 'b')
plt.xlim([(k - 1) * inc, (k + 2) * inc + wlen])
plt.title("(a)当前帧号：" + i)
plt.xlabel("帧长")
plt.ylabel("幅值")
tlabel += 1
x = np.arange((tlabel - 1) * inc, (tlabel - 1) * inc + wlen)
y = signals[tlabel, :]
plt.subplot(412)
plt.plot(x, y, 'b')
plt.xlim([(k - 1) * inc, (k + 2) * inc + wlen])
plt.title("(b)当前帧号：" + str(tlabel))
plt.xlabel("帧长")
plt.ylabel("幅值")
tlabel += 1
x = np.arange((tlabel - 1) * inc, (tlabel - 1) * inc + wlen)
y = signals[tlabel, :]
plt.subplot(413)
plt.plot(x, y, 'b')
plt.xlim([(k - 1) * inc, (k + 2) * inc + wlen])
plt.title("(c)当前帧号：" + str(tlabel))
plt.xlabel("帧长")
plt.ylabel("幅值")
tlabel += 1
x = np.arange((tlabel - 1) * inc, (tlabel - 1) * inc + wlen)
y = signals[tlabel, :]
plt.subplot(414)
plt.plot(x, y, 'b')
plt.xlim([(k - 1) * inc, (k + 2) * inc + wlen])
plt.title("(d)当前帧号：" + str(tlabel))
plt.xlabel("帧长")
plt.ylabel("幅值")
plt.show()
