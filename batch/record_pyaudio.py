import sys
import pyaudio
import wave

CHUNK = 2 ** 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
record_time = 5
output_path = "./output.wav"

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording ...")
frames = []
for i in range(0, int(RATE / CHUNK * record_time)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Done.")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(output_path, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# def audiostart():
#     audio = pyaudio.PyAudio()
#     stream = audio.open(format=pyaudio.paInt16,
#                         rate=44100,
#                         channels=1,
#                         input_device_index=1,
#                         input=True,
#                         frames_per_buffer=1024)
#     return audio, stream
#
#
# def audiostop(audio, stream):
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()
#
#
# def read_plot_data(stream):
#     data = stream.read(1024)
#     return data
#
#
# def rec_exec(file_path):
#     # 録音データをファイルに保存
#     wave_f = wave.open(file_path, 'wb')
#     wave_f.setnchannels(1)
#     wave_f.setsampwidth(2)
#     wave_f.setframerate(44100)
#     wave_f.writeframes(b''.join(rec_data))
#     wave_f.close()
#
#
# if __name__ == '__main__':
#     args = sys.argv
#
#     if len(args) != 1:
#         # Audio インスタンス取得
#         (audio, stream) = audiostart()
#
#         rec_data = []
#         print("Start")
#         # 音声を読み出し
#         while True:
#             try:
#                 data = read_plot_data(stream)
#                 rec_data.append(data)
#             except KeyboardInterrupt:
#                 print("stop")
#                 break
#
#         # Audio デバイスの解放
#         audiostop(audio, stream)
#
#         # 保存実行
#         rec_exec(args[1])
