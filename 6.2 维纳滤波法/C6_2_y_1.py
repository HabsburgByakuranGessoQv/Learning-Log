# 实验要求一：基本维纳滤波算法语音降噪
from SpeechEnh import *

# 读取语音
(fs, data) = wavfile.read('C6_2_y.wav')
data = data - np.mean(data)
data = data / np.max(np.abs(data))
IS = 0.25   # 设置前导无话段长度
wlen = 200  # 设置帧长为25ms
inc = 80    # 设置帧移为10ms
SNR = 5     # 设置信噪比SNR
N = len(data)  # 信号长度
time = [i / fs for i in range(N)]  # 设置时间
r1 = awgn(data, SNR)
NIS = int((IS * fs - wlen) // inc + 1)

# 维纳滤波法
a, b = 4, 0.001
output = weina_Norm(r1, wlen, inc, NIS, a, b)
output = output / np.max(np.abs(output))
# 画图
plt.figure()
plt.subplot(3, 1, 1)
plt.plot(time, data)
plt.title("纯语音波形")
plt.ylabel('幅值')
plt.subplot(3, 1, 2)
plt.plot(time, r1)
plt.title('带噪语音信号')
plt.ylabel('幅值')
plt.subplot(3, 1, 3)
plt.title('基本维纳滤波后波形')
plt.plot(time, output)
plt.ylabel('幅值')
plt.xlabel('时间')

plt.show()