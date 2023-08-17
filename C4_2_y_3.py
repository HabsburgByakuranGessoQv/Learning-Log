from speechlib import *

(fs, data) = wavfile.read('C4_2_y.wav')
data = data - np.mean(data)
data = data / np.max(data)
wlen = 320
inc = 80
N = len(data)
time = [i / fs for i in range(N)]
T1 = 0.05

voiceseg, vsl, SF, Ef, period = pitch_Ceps(data, wlen, inc, T1, fs, miniL=10)
fn = len(SF)
frameTime = FrameTimeC(fn, wlen, inc, fs)

plt.subplot(2, 1, 1)
plt.plot(time, data)
plt.title('语音波形')
plt.ylabel('幅值')
plt.xlabel('时间/s')
plt.subplot(2, 1, 2)
plt.plot(frameTime, period)
plt.title('倒谱法基音周期检测')
plt.ylabel('幅值')
plt.xlabel('时间/s')

for i in range(vsl):
    nx1=voiceseg[i]['start']
    nx2=voiceseg[i]['end']
    plt.subplot(2, 1, 1)
    plt.axvline(frameTime[nx1], np.min(data), np.max(data), color='blue', linestyle='--')
    plt.axvline(frameTime[nx2], np.min(data), np.max(data), color='red', linestyle='-')
    plt.legend(['波形', '起点', '终点'])

    plt.subplot(2, 1, 2)
    plt.axvline(frameTime[nx1], np.min(period), np.max(period), color='blue', linestyle='--')
    plt.axvline(frameTime[nx2], np.min(period), np.max(period), color='red', linestyle='-')
    plt.legend(['基音', '起点', '终点'])

plt.show()