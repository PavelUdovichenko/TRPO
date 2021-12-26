import geturlcontent
import requests
from Google import Create_Service, convert_to_RFC_datetime
import json
import numpy


def main():
    url = geturlcontent.get_url()
    service = create_calendar()
    # list = list_calendars(service)

    create_event(url, service)
    list_events(service)


def list_events(service):
    response = service.calendarList().list(
        maxResults=250,
        showDeleted=False,
        showHidden=False
    ).execute()

    calendarItems = response.get('items')
    # nextPageToken = response.get('nextPageToken')
    for i in range(len(calendarItems)):
        summaries = response.get('items')[i].get('summary')
        if summaries == "Расписание Поликек":
            calendar_trpo_id = response.get('items')[i].get('id')
        else:
            calendar_trpo_id = None
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_trpo_id, pageToken=page_token).execute()
        for event in events['items']:
            print(event['summary'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break


def create_calendar():

    CLIENT_SECRET_FILE = 'client-secret.json'
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


    """To create a calendar"""
    response = service.calendarList().list(
        maxResults=250,
        showDeleted=False,
        showHidden=False
    ).execute()

    # calendar_trpo_id = calendar_response['id']
    calendarItems = response.get('items')
    summaries = []
    for i in range(len(calendarItems)):
        summary = response.get('items')[i].get('summary')
        summaries.append(summary)
    # print (summaries)
    cname = 'Расписание Поликек'

    if cname not in summaries:
        request_body = {
            'summary': 'Расписание Поликек'
        }
        calendar_response = service.calendars().insert(body=request_body).execute()
        print(calendar_response)
        return service
    else:
        print("Такой календарь уже создан" + str(service))
        return service



def delete_calendar(service, calendar_response):
    """To delete a calendar"""
    service.calendars().delete(calendarId=calendar_response['id']).execute()



def list_calendars(service):
    response = service.calendarList().list(
        maxResults=250,
        showDeleted=False,
        showHidden=False
    ).execute()
    num = 0
    calendarItems = response.get('items')
    nextPageToken = response.get('nextPageToken')
    for i in range(len(calendarItems)):
        summaries = response.get('items')[i].get('summary')
        ids = response.get('items')[i].get('id')
        # print(summaries + " " + ids)
        if summaries == "Расписание Поликек":
            num = num + 1

    while nextPageToken:
        response = service.calendarList().list(
            maxResults=250,
            showDeleted=False,
            showHidden=False,
            pageToken=nextPageToken
        ).execute()

        calendarItems = response.get('items')
        nextPageToken = response.get('nextPageToken')
        for i in range(len(calendarItems)):
            summaries = response.get('items')[i].get('summary')
            ids = response.get('items')[i].get('id')
            # print(summaries + " " + ids)
    print(response)

    return num


def create_event(url, service):

    response = service.calendarList().list(
        maxResults=250,
        showDeleted=False,
        showHidden=False
    ).execute()

    calendarItems = response.get('items')
    nextPageToken = response.get('nextPageToken')
    for i in range(len(calendarItems)):
        summaries = response.get('items')[i].get('summary')
        if summaries == "Расписание Поликек":
            calendar_trpo_id = response.get('items')[i].get('id')
        else:
            calendar_trpo_id = None

    """Create an event"""
    colors = service.colors().get().execute()
    # pprint(colors)
    url_response = requests.get(url)
    content = json.loads(url_response.text)

    week = content['days']
    # print(week)
    weeklen = len(week)
    for i in range(weeklen):
        # print(content.get("days")[i].get("date"))
        date = content.get("days")[i].get("date")
        lessons = content.get("days")[i].get("lessons")
        # print(date)
         # print(lessons)
        for j in range(len(lessons)):
            subject = lessons[j].get("subject")
            # print(subject)
            time_start = lessons[j].get("time_start")
            # print(time_start)
            time_end = lessons[j].get("time_end")
            # print(time_end)
            Type = lessons[j].get("typeObj").get("name")
            # print(Type)
            groups = lessons[j].get("groups")
            ftimes = str(date + 'T' + time_start + ':00Z')
            ftimee = str(date + 'T' + time_end + ':00Z')
            for k in range(len(groups)):
                group_num = groups[k].get("name")
                # print(group_num)
            teachers = lessons[j].get("teachers")
            if teachers is None:
                teachers = [{"full_name": 'Тот, кого нельзя называть'}]
            for l in range(len(teachers)):
                teacher_name = teachers[l].get("full_name")
                # print(teacher_name)
            auditories = lessons[j].get("auditories")[0].get("building").get("name")
            # print(auditories)
            lms_url = lessons[j].get("lms_url")
            # print(lms_url)
            result = {
                'StartTime': ftimes,
                'EndTime': ftimee,
                'summary': subject,
                'description': Type + "\n" + group_num + "\n" + teacher_name + "\n" + "URL:" + lms_url,
                'location': auditories,
            }
            # print(result)
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
                'description': Type + " " + group_num + "" + teacher_name,
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
    return print(event_response)

# print(event_response)

if __name__ == "__main__":
	main()
