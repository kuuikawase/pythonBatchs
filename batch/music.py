# -*- coding: utf-8 -*-
import asyncio
import os
import subprocess
import sys
import time

import glob
import wave
import pyaudio
import time
import ffmpeg
from pydub import AudioSegment
from pydub.utils import make_chunks

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import globUtil
from common import fileUtil
from common import propertiesConstants
from common import propertiesUtil
from common import voicevoxUtil

PLAY_STATUS_FILE = propertiesUtil.read_properties(propertiesConstants.MUSIC_PLAY_STATUS)
PLAY_MUSIC_FOLDER = propertiesUtil.read_properties(propertiesConstants.MUSIC_FOLDER)
BREAK = "break"
RETURN_TEXT = ["end", "now", BREAK]


def stop_music():
    with open(PLAY_STATUS_FILE, mode='w', encoding="utf-8") as f:
        f.write(BREAK)


def execution_reservation_music(title):
    with open(PLAY_STATUS_FILE, mode='w', encoding="utf-8") as f:
        f.write(title)


def convert_ffmpeg(text):
    try:
        f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
        read_music_status = f.read()
        f.close()
        wavfile = PLAY_MUSIC_FOLDER + "\\" + read_music_status + r".wav"
        try:
            wf = wave.open(wavfile, "rb")
        except:
            # 入力
            stream = ffmpeg.input(PLAY_MUSIC_FOLDER + read_music_status + r".mp4")
            # 出力
            stream = ffmpeg.output(stream, wavfile)
            # 実行
            ffmpeg.run(stream)
    except:
        pass


def play_music_mp4():
    f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
    read_music_status = f.read()
    f.close()

    print(PLAY_STATUS_FILE)

    # 再生可能でない場合、実行しない
    f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
    read_music_status = f.read()
    f.close()
    if read_music_status in RETURN_TEXT:
        return

    # 再生ファイル読み込み
    try:
        wavfile = PLAY_MUSIC_FOLDER + "\\" + read_music_status + r".wav"
        print(wavfile)
        try:
            wf = wave.open(wavfile, "rb")
        except:
            # mp4の場合、wavに変換
            # 入力
            print(PLAY_MUSIC_FOLDER + "\\" + read_music_status + r".mp4")
            stream = ffmpeg.input(PLAY_MUSIC_FOLDER + "\\" + read_music_status + r".mp4")
            # 出力
            stream = ffmpeg.output(stream, wavfile)
            # 実行
            ffmpeg.run(stream)
    except Exception as e:
        print("実行失敗")
        print(e)
        return

    with open(PLAY_STATUS_FILE, mode='w', encoding="utf-8") as f:
        f.write("now")

    voicevoxUtil.speak_voicevox("音楽を再生します。")
    print(wavfile)
    wf = wave.open(wavfile, "rb")

    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return data, pyaudio.paContinue

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

        f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
        music = f.read()
        f.close()
        if music != "now":
            break

    stream.stop_stream()
    stream.close()
    wf.close()

    f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
    music = f.read()
    f.close()

    if music == "now":
        with open(PLAY_STATUS_FILE, mode='w', encoding="utf-8") as f:
            f.write("end")

    # close PyAudio (7)
    p.terminate()

def play_music():
    f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
    read_music_status = f.read()
    f.close()


    if read_music_status in RETURN_TEXT:
        return

    f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
    read_music_status = f.read()
    f.close()
    wave_flg = False
    mp3_flg = False
    # 再生ファイル読み込み
    try:
        music_stream = wave.open(read_music_status, "rb")
        wave_flg = True
    except Exception as e:
        try:
            music_stream = AudioSegment.from_mp3(read_music_status)
            mp3_flg = True
        except Exception as e:
            print("実行失敗")
            print(e)
            return

    with open(PLAY_STATUS_FILE, mode='w', encoding="utf-8") as f:
        f.write("now")

    voicevoxUtil.speak_voicevox("音楽を再生します。", 8)

    p = pyaudio.PyAudio()

    # waveファイルの場合
    if wave_flg:
        def callback(in_data, frame_count, time_info, status):
            data = music_stream.readframes(frame_count)
            return data, pyaudio.paContinue

        stream = p.open(format=p.get_format_from_width(music_stream.getsampwidth()),
                        channels=music_stream.getnchannels(),
                        rate=music_stream.getframerate(),
                        output=True,
                        stream_callback=callback)

        stream.start_stream()
        while stream.is_active():
            print("stream")
            time.sleep(0.1)

            f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
            music = f.read()
            f.close()
            if music != "now":
                break

        stream.stop_stream()
    # mp3ファイルの場合
    else:
        stream = p.open(format=p.get_format_from_width(music_stream.sample_width),
                        channels=music_stream.channels,
                        rate=music_stream.frame_rate,
                        output=True)
        for chunk in make_chunks(music_stream, 500):
            stream.write(chunk._data)
            f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
            music = f.read()
            f.close()
            if music != "now":
                break

    stream.close()
    music_stream.close()

    f = open(PLAY_STATUS_FILE, "r", encoding="utf-8")
    music = f.read()
    f.close()

    if music == "now":
        with open(PLAY_STATUS_FILE, mode='w', encoding="utf-8") as f:
            f.write("end")

    # close PyAudio (7)
    p.terminate()


def execute():
    # 再生可能状態チェック
    with open(PLAY_STATUS_FILE, mode='r', encoding="utf-8") as f:
        read_music_status = f.read()
    if read_music_status in RETURN_TEXT:
        return

    cmd_file = "python " + os.path.dirname(__file__) + "\\" + "music.py"

    print(cmd_file)

    command = cmd_file

    subprocess.Popen(command)
    print("成功")


if __name__ == '__main__':
    play_music()

# i = 0
# for name in glob.glob('.\mp4\*.mp4'):
#     name = name.replace(".\mp4\\", "")
#     name = name.replace(".mp4", "")
#     if i == 0:
#         i += 1
#         continue
#     batchMusic().music(name)
#     i += 1
#     while True:
#         with open('music.txt', mode='r') as f:
#             text = f.read()
#         if text == "end":
#             break
#         time.sleep(1)
