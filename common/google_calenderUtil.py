import datetime
import re
import googleapiclient.discovery
import google.auth
from common import propertiesConstants
from common import propertiesUtil
from common import voicevoxUtil

SCHEDULE_ADD_TASK_PATH = propertiesUtil.read_properties(propertiesConstants.SCHEDULE_ADD_TASK_PATH)
SCHEDULE_NOW_TASK_PATH = propertiesUtil.read_properties(propertiesConstants.SCHEDULE_NOW_TASK_PATH)


def calender_api_preparation():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    calendar_id = 'kawase0987@gmail.com'

    gapi_creds = google.auth.load_credentials_from_file(
        'credentials.json', SCOPES)[0]

    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=gapi_creds)
    return service, calendar_id


def add_calendar_datetime(title, location, description, startdate, enddate):
    service, calendar_id = calender_api_preparation()
    event = {
        'summary': title,
        'location': location,
        'description': description,
        'start': {
            'dateTime': datetime.datetime(startdate[0], startdate[1], startdate[2], startdate[3],
                                          startdate[4]).isoformat(),
            'timeZone': 'Japan'
        },
        'end': {
            'dateTime': datetime.datetime(enddate[0], enddate[1], enddate[2], enddate[3], enddate[4]).isoformat(),
            'timeZone': 'Japan'
        },
    }
    print(event)
    voicevoxUtil.speak_voicevox("予定を追加します。", 8)
    event = service.events().insert(calendarId=calendar_id, body=event).execute()


def add_calendar_date(title, location, description, startdate, enddate):
    service, calendar_id = calender_api_preparation()
    event = {
        'summary': title,
        'location': location,
        'description': description,
        'start': {
            'date': '{}-{}-{}'.format(startdate[0], startdate[1], startdate[2]),
            'timeZone': 'Japan'
        },
        'end': {
            'date': '{}-{}-{}'.format(enddate[0], enddate[1], enddate[2]),
            'timeZone': 'Japan'
        },
    }
    print(event)
    voicevoxUtil.speak_voicevox("終日で予定を追加します。", 8)
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


def get_write_text_calendar():
    service, calendar_id = calender_api_preparation()

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    event_list = service.events().list(
        calendarId=calendar_id, timeMin=now,
        maxResults=200, singleEvents=True,
        orderBy='startTime').execute()
    print(event_list)
    events = event_list.get('items', [])
    formatted_events = [(event['start'].get('dateTime', event['start'].get('date')),  # start time or day
                         event['end'].get('dateTime', event['end'].get('date')),  # end time or day
                         event['summary'], event.get('dateTime', 'NoData')) for event in events]

    response = ''
    for event in formatted_events:
        if re.match(r'^\d{4}-\d{2}-\d{2}$', event[0]):
            start_date = '{0:%Y-%m-%d}'.format(datetime.datetime.strptime(event[0], '%Y-%m-%d'))
            end_date = '{0:%Y-%m-%d}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%d'))
            response += '{0}|||{1}|||{2}|||{3}|||{4}\n'.format("AllDate", start_date, end_date, event[2], event[3])
        else:
            start_time = '{0:%Y-%m-%d %H:%M}'.format(datetime.datetime.strptime(event[0], '%Y-%m-%dT%H:%M:%S+09:00'))
            end_time = '{0:%Y-%m-%d 0:%H:%M}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S+09:00'))
            response += '{0}|||{1}|||{2}|||{3}|||{4}\n'.format("DateTime", start_time, end_time, event[2], event[3])
    response = response.rstrip('\n')
    print("response")
    print(response)
    with open(SCHEDULE_NOW_TASK_PATH, mode="w", encoding="utf-8") as f:
        f.write(response)


def delete_calendar(start, end, summary, description):
    service, calendar_id = calender_api_preparation()

    now = datetime.datetime.utcnow().isoformat() + 'Z'

    event_list = service.events().list(
        calendarId=calendar_id, timeMin=now,
        maxResults=200, singleEvents=True,
        orderBy='startTime').execute()

    events = event_list.get('items', [])
    delete_list = []
    # 2024-01-11T00:00:00+09:00
    # 2024-01-12T23:59:00+09:00
    # for event_item in events:
    #     if (event_item['start'].get('dateTime', event_item['start'].get('date')) == start
    #             and event_item['end'].get('dateTime', event_item['end'].get('date')) == end
    #             and event_item['summary'] == summary and event_item['description'] == description):
    #         event_id = event_item['id']
    #         service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    #         print("削除" + event_item['id'])
