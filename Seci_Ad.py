import pyaudio
import wave
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

(fs, sound) = wavfile.read("my.wav")
t = np.array([i / fs for i in range(sound.size)])
sound_max = np.absolute(sound).max()
sound = sound / sound_max  # 归一化

noise = 2 * np.random.rand(sound.size) - 1
noise_max = np.absolute(noise).max()
noise = noise / noise_max  # 归一化

new_sound = sound + noise
new_sound_max = np.absolute(new_sound).max()
new_sound = new_sound / new_sound_max

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
plt.plot(t, new_sound)
plt.title('Linear Addition')
plt.ylabel('Normalized Amplitude')
plt.xlabel('Time/s')
plt.show()
