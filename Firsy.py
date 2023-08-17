import pyaudio
import wave
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import *


# 定义数据流参数信息
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
n_frames = int(RATE / CHUNK * RECORD_SECONDS)  # 计算出所需采集帧的数量
WAVE_OUTPUT_FILENAME = "my.wav"

# 音频信号采集
# 实例化一个Pyaudio对象
p = pyaudio.PyAudio()
# 使用该对象打开声卡，并用上述参数信息对数据流进行赋值
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
# 开始录音
print("* recording")

frames = []

for i in range(0, n_frames):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")
# 关闭数据流，声卡；终止Pyaudio
stream.stop_stream()
stream.close()
p.terminate()

# 设定存储录音的WAV文件的基本信息
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


# 读取音频文件
# 只读模式打开需要播放的文件
wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')

# 实例化一个pyaudio对象
p = pyaudio.PyAudio()


# 定义回调函数
def callback(in_data, frame_count, time_info, status):
    temp_data = wf.readframes(frame_count)
    return (temp_data, pyaudio.paContinue)


# 以回调函数的形式打开声卡，创建数据流
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)


# 开始播放
# 打开数据流
stream.start_stream()

# 等待数据流停止
while stream.is_active():
    time.sleep(0.1)

# 停止数据流，关闭声卡、音频文件；终止Pyaudio
stream.stop_stream()
stream.close()
wf.close()
p.terminate()


# 画图
(fs, sound) = wavfile.read(WAVE_OUTPUT_FILENAME)
t = np.array([i/fs for i in range(sound.size)])
plt.plot(t, sound)
plt.title('Sound Wave')
plt.xlabel('Time/s')
plt.ylabel('Amplitude')
plt.show()
