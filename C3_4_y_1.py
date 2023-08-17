# -*- coding: utf-8 -*-
from speechlib import *

(framerate, wave_data) = wavfile.read("C3_4_y_1.wav")

wave_data=wave_data/max(abs(wave_data))
y = wave_data[0:1000]

N = 1024
length = len(y)
time = np.arange(0,length) * (1.0/framerate)
plt.figure(1)
plt.subplot(311)
plt.plot(time,y,'k')
plt.ylabel("幅值")
plt.xlabel("时间/s")
plt.title("(a)信号波形")

z = Nrceps(y)

plt.subplot(312)
plt.plot(time, z, 'k')
plt.axis("tight")
plt.ylabel("幅值")
plt.xlabel("倒频率/s")
plt.title("(b)信号倒谱图")
plt.axis([0,time[512],-0.2,0.2])
plt.grid()

yc=cceps(y)
yn=icceps(yc)
yn=np.real(yn)
plt.subplot(313)
plt.plot(time, yn, 'k')
plt.ylabel("幅值")
plt.xlabel("时间/s")
plt.title("(c)恢复信号")
plt.show()

