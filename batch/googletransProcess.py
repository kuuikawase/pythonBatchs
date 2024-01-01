import shutil
from googletrans import LANGUAGES, Translator
import win32clipboard as w32c
import time  # タイムラグをつける
from ..common import textUtil



def trans_text_file(file_name):
    # file_name = "C:\\Users\\kuui\\Documents\\Paradox Interactive\Stellaris\\mod\\Lustful Void\\localisation\\japanese\\lv_common_l_japanese.yml"
    while True:
        file_name = input("入力：")
        # バックアップファイルの保存
        back_name = file_name + ".bak"
        shutil.copy(file_name, back_name)

        with open(file_name, encoding="utf-8") as f:
            data_lines = f.read()

        # 文字列置換
        fileText = ""
        lists = data_lines.split('"')
        for i, text in enumerate(lists):
            try:
                if i % 2 == 1:
                    translator = Translator()
                    detected_lang = translator.detect(text).lang
                    detected_lang_name = LANGUAGES.get(detected_lang)
                    # transText = translator.translate(text, src=detected_lang, dest='ja').text.encode('utf-8')
                    text = translator.translate(
                        text, src=detected_lang, dest='ja').text
                    print(i / 2)
                    print(text)
            except Exception as e:
                print(e)
            fileText += text + '"'

        # 同じファイル名で保存
        with open(file_name, mode="w", encoding="utf-8") as f:
            f.write(fileText)


def trans_text(text):
    try:
        detected_lang = translator.detect(text).lang
        detected_lang_name = LANGUAGES.get(detected_lang)
        transText = translator.translate(
            text, src=detected_lang, dest='ja').text

        return transText
    except Exception as ex:
        return print(ex)


def trans_clipbord():
    try:
        w32c.OpenClipboard()
        translator = Translator()
        text = w32c.GetClipboardData()
        detected_lang = translator.detect(text).lang
        detected_lang_name = LANGUAGES.get(detected_lang)
        # transText = translator.translate(text, src=detected_lang, dest='ja').text.encode('utf-8')
        transText = translator.translate(
            text, src=detected_lang, dest='ja').text
        # .encode("utf-8")
        print(transText)

        # w32c.EmptyClipboard()
        text2 = 'text'
        # w32c.SetClipboardText(unicode(transText),
        #                   w32c.CF_UNICODETEXT)
        # w32c.SetClipboardText(transText,
        #                       w32c.CF_TEXT)
        return transText
    except Exception as ex:
        return print(ex)
    finally:
        w32c.CloseClipboard()
