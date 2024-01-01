from batch import music
from common import globUtil
from common import fileUtil
from common import propertiesConstants
from common import propertiesUtil
from common import voicevoxUtil
from batch import music
import subprocess
import os
import win32clipboard as w32c
import  time


# これはサンプルの Python スクリプトです。

# Shift+F10 を押して実行するか、ご自身のコードに置き換えてください。
# Shift を2回押す を押すと、クラス/ファイル/ツールウィンドウ/アクション/設定を検索します。

def read():
    try:
        w32c.OpenClipboard()
        text = w32c.GetClipboardData()

        # w32c.EmptyClipboard()
        text2 = 'text'
        # w32c.SetClipboardText(unicode(transText),
        #                   w32c.CF_UNICODETEXT)
        # w32c.SetClipboardText(transText,
        #                       w32c.CF_TEXT)
        return text
    except Exception as ex:
        return print(ex)
    finally:
        w32c.CloseClipboard()


def print_hi(name):
    # スクリプトをデバッグするには以下のコード行でブレークポイントを使用してください。
    print(f'Hi, {name}')  # Ctrl+F8を押すとブレークポイントを切り替えます。


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    print_hi('PyCharm')

    # PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください

    # url = "https://youtu.be/S9wXcIOHLyk?si=ajwc5GAsRo7AHmvb"
    # youtubeDownload.youtube_download_and_move_file(url, os.path.dirname(__file__))

    # print(globUtil.search(os.path.dirname(__file__), "mp4"))
    # text_list = globUtil.search_keyword_file("E:\\python\\mp4", "mp4", "Marsh")
    # print(text_list)
    # music.execution_reservation_music(text_list[0])
    # #
    # voicevoxUtil.speakvoicevox("コードを実行します。")

    # mp4 = \
    #     "「ＲＩＣＫＹ☆ＳＴＡＲ」もってけ！リックロール (Motteke! Rikku Rōru)"
    # music.execution_reservation_music(mp4)

    # music.stop_music()

    music.play_music()
    #
    # pre_seq = None
    #
    # while True:
    #     seq = w32c.GetClipboardSequenceNumber()
    #
    #     if pre_seq != seq:
    #         text = read()
    #         pre_seq = seq
    #         voicevoxUtil.speak_voicevox(text, 8)
    #     time.sleep(10)
    #


