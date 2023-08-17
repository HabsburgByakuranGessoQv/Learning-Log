# 实验要求二：基本先验信噪比的维纳滤波算法语音降噪
from SpeechEnh import *

(fs, data) = wavfile.read('C6_2_y.wav')
data =data- np.mean(data)
data = data/np.max(np.abs(data)) # 幅值归一化
IS = 0.25  # 设置前导无话段长度
wlen = 200  # 设置帧长为25ms
inc = 80  # 设置帧移为10msho
SNR = 5  # 设置信噪比SNR
NIS = int((IS * fs - wlen) // inc + 1)
alpha = 0.95
N = len(data)  # 信号长度
time = [i / fs for i in range(N)]  # 设置时间
signal = awgn(data, SNR)
output = weina_Im(data,wlen,inc,NIS,alpha)
output = output / np.max(np.abs(output))

# 画图
plt.subplot(3, 1, 1)
plt.plot(time, data)
plt.title('原始信号')
plt.ylabel('幅值')
plt.subplot(3, 1, 2)
plt.plot(time, signal)
plt.title('加噪声信号')
plt.ylabel('幅值')
plt.subplot(3, 1, 3)
plt.plot(time, output)
plt.title('改进维纳滤波后信号')
plt.ylabel('幅值')
plt.xlabel('时间')
plt.show()