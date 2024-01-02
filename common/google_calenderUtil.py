import datetime
import re
import googleapiclient.discovery
import google.auth
from common import propertiesConstants
from common import propertiesUtil
from common import voicevoxUtil

SCHEDULE_PATH = propertiesUtil.read_properties(propertiesConstants.SCHEDULE_PATH)


def add_calendar(title, location, description, startdate, enddate):
    # 編集スコープの設定(今回は読み書き両方OKの設定)
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # カレンダーIDの設定(基本的には自身のgmailのアドレス)
    calendar_id = 'kawase0987@gmail.com'

    # 認証ファイルを使用して認証用オブジェクトを作成
    gapi_creds = google.auth.load_credentials_from_file(
        'credentials.json', SCOPES)[0]

    # 認証用オブジェクトを使用してAPIを呼び出すためのオブジェクト作成
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=gapi_creds)

    # # 追加するスケジュールの情報を設定
    # event = {
    #     # 予定のタイトル
    #     'summary': 'テスト！',
    #     'location': 'ここ',
    #     'description': 'テスト詳細',
    #     # 予定の開始時刻(ISOフォーマットで指定)
    #     'start': {
    #         'dateTime': datetime.datetime(2023, 3, 14, 0, 00).isoformat(),
    #         'timeZone': 'Japan'
    #     },
    #     # 予定の終了時刻(ISOフォーマットで指定)
    #     'end': {
    #         'dateTime': datetime.datetime(2023, 3, 14, 17, 59).isoformat(),
    #         'timeZone': 'Japan'
    #     },
    # }
    # 追加するスケジュールの情報を設定
    event = {
        # 予定のタイトル
        'summary': title,
        'location': location,
        'description': description,
        # 予定の開始時刻(ISOフォーマットで指定)
        'start': {
            'dateTime': datetime.datetime(startdate[0], startdate[1], startdate[2], startdate[3],
                                          startdate[4]).isoformat(),
            'timeZone': 'Japan'
        },
        # 予定の終了時刻(ISOフォーマットで指定)
        'end': {
            'dateTime': datetime.datetime(enddate[0], enddate[1], enddate[2], enddate[3], enddate[4]).isoformat(),
            'timeZone': 'Japan'
        },
    }
    print(event)
    # 予定を追加する
    event = service.events().insert(calendarId=calendar_id, body=event).execute()


def read_text_calendar():
    flg = ""
    with open(SCHEDULE_PATH, mode='r', encoding="utf-8") as f:
        flg = f.read()
    print(flg)
    if flg:
        print("true")
        schedule_lists = flg.split(":")
        startdate = schedule_lists[2].split(",")
        startdate = [int(startdate[0]), int(startdate[1]), int(startdate[2]), int(startdate[3]), int(startdate[4])]
        enddate = schedule_lists[3].split(",")
        enddate = [int(enddate[0]), int(enddate[1]), int(enddate[2]), int(enddate[3]), int(enddate[4])]
        print(startdate, enddate)
        try:
            add_calendar(schedule_lists[0], "", schedule_lists[1], startdate, enddate)
            with open(SCHEDULE_PATH, mode='w', encoding="utf-8") as f:
                f.write("")
        except Exception as e:
            print(e)
