import geturlcontent
import requests
from Google import Create_Service, convert_to_RFC_datetime
import json

url = geturlcontent.get_url()
response = requests.get(url)


CLIENT_SECRET_FILE = 'client-secret.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

request_body = {
    'summary': 'Расписание Поликек'
}
"""To create a calendar"""
calendar_response = service.calendars().insert(body=request_body). execute()
print(calendar_response)
calendar_trpo_id = calendar_response['id']


"""To delete a calendar"""
# service.calendars().delete(calendarId=calendar_response['id']).execute()

"""Create an event"""
colors = service.colors().get().execute()
# pprint(colors)
response = requests.get(url)
content = json.loads(response.text)

week = content['days']
print(week)
weeklen = len(week)
for i in range(weeklen):
    # print(content.get("days")[i].get("date"))
    date = content.get("days")[i].get("date")
    lessons = content.get("days")[i].get("lessons")
    # print(date)
     # print(lessons)
    for j in range(len(lessons)):
        subject = lessons[j].get("subject")
        print(subject)
        time_start = lessons[j].get("time_start")
        print(time_start)
        time_end = lessons[j].get("time_end")
        print(time_end)
        Type = lessons[j].get("typeObj").get("name")
        print(Type)
        groups = lessons[j].get("groups")
        ftimes = str(date + 'T' + time_start + ':00Z')
        ftimee = str(date + 'T' + time_end + ':00Z')
        for k in range(len(groups)):
            group_num = groups[k].get("name")
            print(group_num)
        teachers = lessons[j].get("teachers")
        if teachers is None:
            teachers = [{"full_name": 'Тот, кого нельзя называть'}]
        for l in range(len(teachers)):
            teacher_name = teachers[l].get("full_name")
            print(teacher_name)
        auditories = lessons[j].get("auditories")[0].get("building").get("name")
        print(auditories)
        lms_url = lessons[j].get("lms_url")
        print(lms_url)
        event_request_body = {
            'start': {
                'dateTime': ftimes,
                'timeZone': 'Europe/Moscow'
            },
            'end': {
                'dateTime': ftimee,
                'timeZone': 'Europe/Moscow'
            },
            'summary': subject,
            'description': Type + group_num + teacher_name,
            'colorId': 5,
            'status': 'confirmed',
            'transparency': 'opaque',
            'visibility': 'private',
            'location': auditories,
            # 'attendees': [
            #     {
            #         'displayName': 'JJ',
            #         'comment': 'I enjoy coding',
            #         'email': 'Udovichenkop@gmail.com',
            #         'optional': False,
            #         'organizer': False,
            #         'responseStatus': 'accepted',
            #     }
            # ]
        }

        maxAttendees = 5
        sendNotification = True
        sendUpdate = 'none'
        supportsAttachments = True

        event_response = service.events().insert(
            calendarId=calendar_trpo_id,
            maxAttendees=maxAttendees,
            sendNotifications=sendNotification,
            sendUpdates=sendUpdate,
            supportsAttachments=supportsAttachments,
            body=event_request_body
        ).execute()

hour_adjustment = -3


# print(event_response)
