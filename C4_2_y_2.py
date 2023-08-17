# 4.2.2
from speechlib import *
from scipy.signal import ellipord, ellip, freqz

fs = 8000
fs2 = fs / 2
Wp = np.array([60, 500]) / fs2
Ws = np.array([20, 1500]) / fs2
Rp = 1
Rs = 40
n, Wn = ellipord(Wp, Ws, Rp, Rs)
b, a = ellip(n, Rp, Rs, Wn, 'bandpass')

w, H = freqz(b, a)

mag = np.abs(H)
db = 20 * np.log10((mag + 1e-20) / np.max(mag))

plt.plot(w / np.pi * fs2, db)
plt.xlabel('频率/Hz')
plt.ylabel('幅值/dB')
plt.ylim([-90, 10])
plt.xlim([0, fs2])
plt.title('椭圆滤波器频率响应')
plt.show()