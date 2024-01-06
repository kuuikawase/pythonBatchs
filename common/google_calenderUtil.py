import datetime
import re
import googleapiclient.discovery
import google.auth
from common import propertiesConstants
from common import propertiesUtil
from common import voicevoxUtil

SCHEDULE_ADD_TASK_PATH = propertiesUtil.read_properties(propertiesConstants.SCHEDULE_ADD_TASK_PATH)
SCHEDULE_NOW_TASK_PATH = propertiesUtil.read_properties(propertiesConstants.SCHEDULE_NOW_TASK_PATH)

def add_calendar_datetime(title, location, description, startdate, enddate):
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
    voicevoxUtil.speak_voicevox("予定を追加します。", 8)
    # 予定を追加する
    event = service.events().insert(calendarId=calendar_id, body=event).execute()

def add_calendar_date(title, location, description, startdate, enddate):
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

    # 追加するスケジュールの情報を設定
    event = {
        # 予定のタイトル
        'summary': title,
        'location': location,
        'description': description,
        # 予定の開始時刻(ISOフォーマットで指定)
        'start': {
            'date': '{}-{}-{}'.format(startdate[0], startdate[1], startdate[2]),
            'timeZone': 'Japan'
        },
        # 予定の終了時刻(ISOフォーマットで指定)
        'end': {
            'date': '{}-{}-{}'.format(enddate[0], enddate[1], enddate[2]),
            'timeZone': 'Japan'
        },
    }
    print(event)
    voicevoxUtil.speak_voicevox("予定を追加します。", 8)
    # 予定を追加する
    event = service.events().insert(calendarId=calendar_id, body=event).execute()


def read_text_calendar():
    flg = ""
    with open(SCHEDULE_ADD_TASK_PATH, mode='r', encoding="utf-8") as f:
        flg = f.read()
    if flg:
        print("true")
        schedule_lists = flg.split(":")
        startdate = schedule_lists[2].split(",")
        startdate = [int(startdate[0]), int(startdate[1]), int(startdate[2]), int(startdate[3]), int(startdate[4])]
        enddate = schedule_lists[3].split(",")
        enddate = [int(enddate[0]), int(enddate[1]), int(enddate[2]), int(enddate[3]), int(enddate[4])]
        try:
            if int(startdate[3]) == 0 and int(startdate[4]) == 0 and int(enddate[3]) == 23 and int(enddate[4]) == 59:
                add_calendar_datetime(schedule_lists[0], "", schedule_lists[1], startdate, enddate)
            else:
                add_calendar_datetime(schedule_lists[0], "", schedule_lists[1], startdate, enddate)
            with open(SCHEDULE_ADD_TASK_PATH, mode='w', encoding="utf-8") as f:
                f.write("")
        except Exception as e:
            print(e)

def write_text_calendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # カレンダーIDの設定(基本的には自身のgmailのアドレス)
    calendar_id = 'kawase0987@gmail.com'

    # Googleの認証情報をファイルから読み込む
    gapi_creds = google.auth.load_credentials_from_file(
        'credentials.json', SCOPES)[0]

    # 認証用オブジェクトを使用してAPIを呼び出すためのオブジェクト作成
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=gapi_creds)

    # ②Googleカレンダーからイベントを取得する
    # 現在時刻を世界協定時刻（UTC）のISOフォーマットで取得する
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    # 直近3件のイベントを取得する
    event_list = service.events().list(
        calendarId=calendar_id, timeMin=now,
        maxResults=200, singleEvents=True,
        orderBy='startTime').execute()

    # ③イベントの開始時刻、終了時刻、概要を取得する
    events = event_list.get('items', [])
    print(events)
    formatted_events = [(event['start'].get('dateTime', event['start'].get('date')),  # start time or day
                         event['end'].get('dateTime', event['end'].get('date')),  # end time or day
                         event['summary']) for event in events]

    # ④出力テキストを生成する
    response = ''
    # データの正規化をする
    for event in formatted_events:
        if re.match(r'^\d{4}-\d{2}-\d{2}$', event[0]):
            start_date = '{0:%Y-%m-%d}\n'.format(datetime.datetime.strptime(event[1], '%Y-%m-%d'))
            response += '{0}\n{1}\n{2}\n'.format("AllDate", start_date, event[2])
        else:
            start_time = '{0:%Y-%m-%d %H:%M}\n'.format(datetime.datetime.strptime(event[0], '%Y-%m-%dT%H:%M:%S+09:00'))
            end_time = '{0:%H:%M}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S+09:00'))
            response += '{0}\n{1}\n{2}\n{3}\n'.format("DateTime", start_time, end_time, event[2])
    response = response.rstrip('\n')
    print(response)
    with open(SCHEDULE_NOW_TASK_PATH, mode="w", encoding="utf-8") as f:
        f.write(response)

if __name__ == "__main__":
    write_text_calendar()