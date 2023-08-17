# 实验要求一：谱减法语音降噪
from SpeechEnh import *
# 读取语音
(fs, data) = wavfile.read('C6_1_y.wav')

data =data- np.mean(data)
data = data/np.max(np.abs(data))  # 幅值归一化
IS = 0.25       # 设置前导无话段长度
wlen = 200      # 设置帧长为25ms
inc = 80        # 设置帧移为10ms
SNR = 5         # 设置信噪比SNR
N = len(data)  # 信号长度
time = [i / fs for i in range(N)]  # 设置时间
signal = awgn(data, SNR)           # 叠加噪声
NIS = int((IS * fs - wlen) // inc + 1)   # 求前导无话段帧数

snr1 = SNR_Calc(data, signal)      # 计算初始信噪比
a, b = 4, 0.001

# 谱减法
output = SpectralSub(signal, wlen, inc, NIS, a, b)
# output =output- np.mean(output)
# output = output/np.max(np.abs(output))
snr2 = SNR_Calc(data, output)      # 计算谱减后信噪比
time1 = [i / fs for i in range(len(output))]

print('加入噪声SNR:{:.4f}\t基本谱减滤波后噪声SNR:{:.4f}\tSNR提升:{:.4f}'.format(snr1, snr2, snr2 - snr1))

# 画图
plt.figure()
plt.subplot(3, 1, 1)
plt.plot(time, data)
plt.ylabel("幅值")
plt.title('纯语音波形')
plt.subplot(3, 1, 2)
plt.plot(time, signal)
plt.title('带噪语音波形')
plt.ylabel("幅值")
plt.subplot(3, 1, 3)
plt.title('谱减后波形')
plt.plot(time1, output)
plt.ylabel("幅值")
plt.xlabel("时间")

plt.show()
