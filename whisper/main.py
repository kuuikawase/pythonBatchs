from audio_transcriber import AudioTranscriber
from audio_utils import display_valid_input_devices, get_valid_input_devices

# 参考　：　https://qiita.com/reriiasu/items/920227cf604dfb8b7949
if __name__ == "__main__":
    transcriber = AudioTranscriber()

    valid_devices = get_valid_input_devices()
    print("使用可能なオーディオデバイス:")
    display_valid_input_devices(valid_devices)

    # 対象のDeviceIndexを入力
    selected_device_index = int(input("対象のDeviceIndexを入力してください: "))

    # 文字起こしを開始
    transcriber.start_transcription(selected_device_index)