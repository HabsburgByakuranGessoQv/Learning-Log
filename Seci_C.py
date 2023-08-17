# 卷积噪声
# from speechlib import *
import pyaudio
import wave
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import *

(fs, sound) = wavfile.read("my.wav")
t = np.array([i / fs for i in range(sound.size)])
sound_max = np.absolute(sound).max()
sound = sound / sound_max

noise = 2 * np.random.rand(sound.size) - 1
noise_max = np.absolute(noise).max()
noise = noise / noise_max

new_sound = np.convolve(sound, noise)
new_sound_max = np.absolute(new_sound).max()
new_sound = new_sound / new_sound_max
t2 = np.array([i / fs for i in range(new_sound.size)])

plt.figure(1)
plt.subplot(311)
plt.plot(t, sound)
plt.title('Original Signal')
plt.ylabel('Normalized Amplitude')
plt.subplot(312)
plt.plot(t, noise)
plt.title('Random Sequence')
plt.ylabel('Normalized Amplitude')
plt.subplot(313)
plt.plot(t2, new_sound)
plt.title('CONV Addition')
plt.ylabel('Normalized Amplitude')
plt.xlabel('Time/s')
plt.show()
