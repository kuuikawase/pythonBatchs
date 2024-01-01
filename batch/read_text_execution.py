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
import csv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import globUtil
from common import fileUtil
from common import propertiesConstants
from common import propertiesUtil
from common import voicevoxUtil
from batch import music
from common import weather

read_path = propertiesUtil.read_properties(propertiesConstants.READ_LISTEN_TEXT_PATH)
time_path = propertiesUtil.read_properties(propertiesConstants.TIME_PATH)


def execution_music(keyword):
    text_list = globUtil.search_keyword_file("E:\\python\\mp4", "mp4", keyword)
    print(text_list)
    music.execution_reservation_music(text_list[0])


def read_text():
    text = ""
    with open(read_path, mode='r', encoding="utf-8") as f:
        text = f.read()
    if "再生" in text:
        print("テスト")


def csv_read(path):
    l = []
    with open(path) as f:
        reader = csv.DictReader(f)
        l = [row for row in reader]
    print(l)
    return l

def time_csv_read():
    return csv_read(time_path)

def execution_wether():
    weathers, valids = weather.weather("石川県")
    weathers[0] = weathers[0].replace("後", "のち")
    weathers[1] = weathers[1].replace("後", "のち")
    voicevoxUtil.speak_voicevox("今日の天気予報は" + weathers[0] + "で、", 8)
    voicevoxUtil.speak_voicevox("明日の天気予報は" + weathers[1] + "です。", 8)


if __name__ == '__main__':
    execution_wether()
