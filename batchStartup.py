import asyncio
import concurrent
import concurrent.futures

from batch import music
from common import globUtil
from common import fileUtil
from common import propertiesConstants
from common import propertiesUtil
from batch import music
from batch import read_text_execution
from common import voicevoxUtil
import subprocess
import time
import datetime
from common import google_calenderUtil


# async def music_excute():
#     while True:
#         await music.execute()
#         await asyncio.sleep(1)
#         print("test")


# pycharmで実行できないバッチ監視
# if __name__ == '__main__':
#     # asyncio.get_event_loop().run_in_executor(None, music())
#     asyncio.run(music_excute())
#     print("test33")

# async def main():
#     loop = asyncio.get_running_loop()
#     with concurrent.futures.ProcessPoolExecutor(max_workers=1) as pool:
#         await loop.run_in_executor(pool, music.execute())
#         await asyncio.sleep(1)
#         # task2 = loop.run_in_executor(pool, func2)
#         # result1 = await task1
#         # result2 = await task2
#         # print('result:', result1, result2)

def batch_list(batch_no):
    print(batch_no)
    # 音楽再生バッチ
    if batch_no == 1:
        print("music")
        music.play_music()
    # googleカレンダー予定追加バッチ
    elif batch_no == 2:
        print("addSchedule")
        google_calenderUtil.read_text_calendar()
        google_calenderUtil.write_text_calendar()
    # 天気予報バッチ
    elif batch_no == 3:
        print("weather")
        # read_text_execution.execution_wether()

def hour_batch_list(batch_no):
    print(batch_no)
    now_h = str(int(datetime.datetime.now().strftime('%H')))

    if batch_no == 1:
        print("now", now_h)
        print(str(now_h) + "時に")
        voicevoxUtil.speak_voicevox("" + now_h + "時になりました。", 8)

def day_batch_list(batch_no):
    print(batch_no)
    if batch_no == 1:
        print("weather")
        # read_text_execution.execution_wether()

async def main():
    day = ""
    hour = ""
    while True:
        # ProcessPoolExecutor の場合
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # 関数に渡す引数のリスト
            args = [1,2,3]

            # map() を使って関数を並行実行し、結果を受け取る
            print(args)
            # results = executor.map(music.play_music(), args)
            results = executor.map(batch_list, args)
            time.sleep(1)
            # for result in results:
            #     print(result)
        #
        # times = read_text_execution.time_csv_read()[0]
        # day = times["day"]
        # hour = times["hour"]
        # now_d = datetime.datetime.now().strftime('%Y/%m/%d')
        # now_h = datetime.datetime.now().strftime('%H')
        # if day != now_d:
        #     with concurrent.futures.ProcessPoolExecutor() as executor:
        #         # 関数に渡す引数のリスト
        #         args = [1]
        #
        #         # map() を使って関数を並行実行し、結果を受け取る
        #         print(args)
        #         # results = executor.map(music.play_music(), args)
        #         results = executor.map(day_batch_list, args)
        #         time.sleep(1)
        # if hour != now_h:
        #     with concurrent.futures.ProcessPoolExecutor() as executor:
        #         # 関数に渡す引数のリスト
        #         args = [1]
        #
        #         # map() を使って関数を並行実行し、結果を受け取る
        #         print(args)
        #         # results = executor.map(music.play_music(), args)
        #         results = executor.map(hour_batch_list, args)
        #         time.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
