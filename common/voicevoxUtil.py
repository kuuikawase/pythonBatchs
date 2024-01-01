import requests  # APIを使う
import json  # APIで取得するJSONデータを処理する
import pyaudio  # wavファイルを再生する
import time  # タイムラグをつける
import win32clipboard as w32c


def speak_voicevox(text, speaker_no):
    if speaker_no is None:
        speaker_no = 8
    # 音声合成クエリの作成
    res1 = requests.post('http://127.0.0.1:50021/audio_query',
                         params={'text': text, 'speaker': speaker_no})
    # 音声合成データの作成
    res2 = requests.post('http://127.0.0.1:50021/synthesis',
                         params={'speaker': speaker_no}, data=json.dumps(res1.json()))
    #
    data = res2.content

    # PyAudioのインスタンスを生成
    p = pyaudio.PyAudio()

    # ストリームを開く
    stream = p.open(format=pyaudio.paInt16,  # 16ビット整数で表されるWAVデータ
                    channels=1,  # モノラル
                    rate=24000,  # サンプリングレート
                    output=True)

    # 再生を少し遅らせる（開始時ノイズが入るため）
    time.sleep(0.2)  # 0.2秒遅らせる

    # WAV データを直接再生する
    stream.write(data)

    # ストリームを閉じる
    stream.stop_stream()
    stream.close()

    # PyAudio のインスタンスを終了する
    p.terminate()


# speakvoicevox(
#    "得意なことはしゃべることです。なまむぎなまごめなまたまごwavファイルを作らずに直接音声を出力することもできます。pythonでwavファイルを出力するにはpyaudioを使います。")
