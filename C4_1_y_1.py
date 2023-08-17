from speechlib import *
(fs, data) = wavfile.read('C4_1_y.wav')
data1 = data/np.max(np.abs(data))                # 幅值归一化

N = len(data1)
wlen = 200
inc = 80
IS = 0.1
overlap = wlen - inc
NIS = int((IS * fs - wlen) // inc + 1)
fn = (N - wlen) // inc + 1

frameTime = FrameTimeC(fn, wlen, inc, fs)
time = [i / fs for i in range(N)]

voiceseg, vsl, SF, NF, amp, zcr = vad_TwoThr(data1, wlen, inc, NIS)

plt.subplot(3, 1, 1)
plt.plot(time, data1)
plt.title('双门限法的端点检测')
plt.ylabel('幅值')
plt.xlabel('时间/s')

plt.subplot(3, 1, 2)
plt.plot(frameTime, amp)
plt.title('短时能量')
plt.ylabel('幅值')
plt.xlabel('时间/s')

plt.subplot(3, 1, 3)
plt.plot(frameTime, zcr)
plt.title('短时过零率')
plt.ylabel('幅值')
plt.xlabel('时间/s')

for i in range(vsl):
    nx1=voiceseg[i]['start']
    nx2=voiceseg[i]['end']
    plt.subplot(3, 1, 1)
    plt.axvline(frameTime[nx1], np.min(data1), np.max(data1), color='blue', linestyle='--')
    plt.axvline(frameTime[nx2], np.min(data1), np.max(data1), color='red', linestyle='-')
    plt.legend(['波形', '起点', '终点'])

    plt.subplot(3, 1, 2)
    plt.axvline(frameTime[nx1], np.min(amp), np.max(amp), color='blue', linestyle='--')
    plt.axvline(frameTime[nx2], np.min(amp), np.max(amp), color='red', linestyle='-')
    plt.legend(['短时能量', '起点', '终点'])

    plt.subplot(3, 1, 3)
    plt.axvline(frameTime[nx1], np.min(zcr), np.max(zcr), color='blue', linestyle='--')
    plt.axvline(frameTime[nx2], np.min(zcr), np.max(zcr), color='red', linestyle='-')
    plt.legend(['短时过零率', '起点', '终点'])

plt.show()


