from speechlib import *

(fs, data) = wavfile.read('C4_2_y.wav')
data = data - np.mean(data)
data = data / np.max(data)
wlen = 320
inc = 80
N = len(data)
time = [i / fs for i in range(N)]
T1 = 0.05

# 4.2.1
voiceseg, vosl, SF, Ef = pitch_vad(data, wlen, inc, T1)
fn = len(SF)
frameTime = FrameTimeC(fn, wlen, inc, fs)

plt.figure(figsize=(14, 8))

plt.subplot(5, 1, 1)
plt.plot(time, data)
plt.subplot(5, 1, 2)
plt.plot(frameTime, Ef)
for i in range(vosl):
    plt.subplot(5, 1, 2)
    plt.plot(frameTime[voiceseg[i]['start']], Ef[voiceseg[i]['start']], '.k')
    plt.plot(frameTime[voiceseg[i]['end']], Ef[voiceseg[i]['start']], 'or')
    plt.legend(['能熵比', 'start', 'end'])

# 4.2.3
voiceseg, vsl, SF, Ef, period = pitch_Ceps(data, wlen, inc, T1, fs, miniL=10)
plt.subplot(5, 1, 3)
plt.plot(frameTime, period)
for i in range(vsl):
    plt.subplot(5, 1, 3)
    plt.plot(frameTime[voiceseg[i]['start']], Ef[voiceseg[i]['start']], '.k')
    plt.plot(frameTime[voiceseg[i]['end']], Ef[voiceseg[i]['start']], 'or')
    plt.legend(['倒谱法', 'start', 'end'])

# 4.2.4
voiceseg, vsl, SF, Ef, period = pitch_Corr(data, wlen, inc, T1, fs)
plt.subplot(5, 1, 4)
plt.plot(frameTime, period)
for i in range(vsl):
    plt.subplot(5, 1, 4)
    plt.plot(frameTime[voiceseg[i]['start']], Ef[voiceseg[i]['start']], '.k')
    plt.plot(frameTime[voiceseg[i]['end']], Ef[voiceseg[i]['start']], 'or')
    plt.legend(['自相关', 'start', 'end'])

# 4.2.5
p = 12
voiceseg, vsl, SF, Ef, period = pitch_Lpc(data, wlen, inc, T1, fs, p)
plt.subplot(5, 1, 5)
plt.plot(frameTime, period)
for i in range(vsl):
    plt.subplot(5, 1, 5)
    plt.plot(frameTime[voiceseg[i]['start']], Ef[voiceseg[i]['start']], '.k')
    plt.plot(frameTime[voiceseg[i]['end']], Ef[voiceseg[i]['start']], 'or')
    plt.legend(['线性预测', 'start', 'end'])

plt.show()