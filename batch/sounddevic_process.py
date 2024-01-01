import sounddevice as sd
import soundfile as sf
import numpy as np

# device_list = sd.query_devices()
# print(device_list)
#
# for device_number in sd.default.device:
#     print(device_number)
#     print(device_list[device_number])
#
# duration = 3  # 3秒間録音する
#
# # デバイス情報関連
# sd.default.device = [3, 7] # Input, Outputデバイス指定
# input_device_info = sd.query_devices(device=sd.default.device[1])
# sr_in = int(input_device_info["default_samplerate"])
# print(duration * sr_in)
#
# # sd.default.samplerate = sr_in
# # sd.default.channels = 1
#
# # 録音
# # myrecording = sd.rec(int(duration * sr_in), samplerate=sr_in, channels=2)
# myrecording = sd.rec(int(duration * sr_in), samplerate=sr_in, channels=1)
# sd.wait() # 録音終了待ち
#
# print(myrecording.shape) #=> (duration * sr_in, channels)
#
# # 録音信号のNumPy配列をwav形式で保存
# sf.write("./myrecording.wav", myrecording, sr_in)

device_list = sd.query_devices()
print(device_list)

fs = 48000
duration = 10  # seconds

sd.default.samplerate = fs
sd.default.channels = 2

myrecording = sd.rec(int(duration * fs))

sd.wait()

sf.write("./myrecording.wav", myrecording, fs)

