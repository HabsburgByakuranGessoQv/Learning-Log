# 实验要求一：boll改进谱减法
from SpeechEnh import *

(fs, data) = wavfile.read('C6_1_y.wav')
data =data- np.mean(data)
data = data/np.max(np.abs(data)) # 幅值归一化
SNR = 10
signal = awgn(data, SNR)
N = len(data)  # 信号长度
time = [i / fs for i in range(N)]  # 设置时间
IS = 0.15   # 设置前导无话段长度
wlen = 200  # 设置帧长为25ms
inc = 80    # 设置帧移为10ms
Gamma=1
Beta=0.03
NIS = int((IS * fs - wlen) // inc + 1)
output = SpectralSubIm(signal, wlen, inc, NIS, Gamma, Beta)
output = output/np.max(np.abs(output))
time1 = [i / fs for i in range(len(output))]

plt.figure()
plt.subplot(3, 1, 1)
plt.plot(time, data)
plt.title('原始信号')
plt.ylabel('幅值')
plt.xlabel('时间/s')
plt.subplot(3, 1, 2)
plt.plot(time, signal)
plt.title('加噪声信号')
plt.ylabel('幅值')
plt.xlabel('时间/s')
plt.subplot(3, 1, 3)
plt.plot(time1,output)
plt.title('滤波信号')
plt.ylabel('幅值')
plt.xlabel('时间/s')
plt.show()



























































