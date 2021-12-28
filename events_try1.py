import geturlcontent
import requests
from Google import Create_Service, convert_to_RFC_datetime
import json
import time


def main():
    url = geturlcontent.get_url()
    service, c_id = create_calendar()
    # list = list_calendars(service)
    create_event(url, c_id, service)
    # list_events(service, c_id)
    rday = get_refresh()
    if rday == 'Monday':
        schedule.every().monday.do(create_event(url, c_id, service))
    elif rday == 'Tuesday':
        schedule.every().tuesday.do(create_event(url, c_id, service))
    elif rday == 'Wednesday':
        schedule.every().wednesday.do(create_event(url, c_id, service))
    elif rday == 'Thursday':
        schedule.every().thursday.do(create_event(url, c_id, service))
    elif rday == 'Friday':
        schedule.every().friday.do(create_event(url, c_id, service))
    elif rday == 'Saturday':
        schedule.every().saturday.do(create_event(url, c_id, service))
    elif rday == 'Sunday':
        schedule.every().sunday.do(create_event(url, c_id, service))


def get_refresh():
    answers = geturlcontent.get_answers()
    day = answers[6]
    return day

def list_events(service, c_id):
    list_events = []
    page_token = None

    while True:
        events = service.events().list(calendarId=c_id, pageToken=page_token).execute()
        for event in events['items']:
            # print("событие" + event['summary'])
            event_list = {
                'StartTime': event['start']['dateTime'],
                'EndTime': event['end']['dateTime'],
                'summary': event['summary'],
                'description': event['description'],
                'location': event['location'],
            }
            list_events.append(event_list)
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    #print("лист создан " + "события: " + str(list_events))

    return list_events



def create_calendar():

    CLIENT_SECRET_FILE = 'client-secret.json'
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    """To create a calendar"""
    list_response = service.calendarList().list(
        maxResults=250,
        showDeleted=False,
        showHidden=False
    ).execute()

    # calendar_trpo_id = calendar_response['id']
    calendarItems = list_response.get('items')
    summaries = []
    for i in range(len(calendarItems)):
        summary = list_response.get('items')[i].get('summary')
        summaries.append(summary)
    # print (summaries)
    cname = 'Расписание Поликек'

    if cname not in summaries:
        request_body = {
            'summary': 'Расписание Поликек'
        }

        calendar_response = service.calendars().insert(body=request_body).execute()
        calendar_trpo_id = calendar_response['id']
        #print(calendar_response)
        return service, calendar_trpo_id
    else:
        print("Такой календарь уже создан")
        for j in range(len(calendarItems)):
            id = list_response.get('items')[j].get('id')
            name = list_response.get('items')[j].get('summary')
            if name == "Расписание Поликек":
                calendar_trpo_id = id
        return service, calendar_trpo_id



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


def create_event(url, c_id, service):
    answers = geturlcontent.get_answers()
    ntf = answers[5]
    add_discription = answers[7]
    calendar_trpo_id = c_id
    """Create an event"""
    # url_response = requests.get(url)
    # content = json.loads(url_response.text)
    fin_content = []
    exists = list_events(service, c_id)
    print("сйечас есть " + str(exists))
    for i in range(len(url)):
        url_response = requests.get(url[i])
        content = json.loads(url_response.text)
        # fin_content.append(content)
        # for j in range(len(fin_content)):
        week = content['days']
        for r in range(len(week)):
            date = content.get("days")[r].get("date")
            lessons = content.get("days")[r].get("lessons")
            for k in range(len(lessons)):
                subject = lessons[k].get("subject")
                time_start = lessons[k].get("time_start")
                time_end = lessons[k].get("time_end")
                Type = lessons[k].get("typeObj").get("name")
                groups = lessons[k].get("groups")
                ftimes = str(date + 'T' + time_start + ':00Z')
                ftimee = str(date + 'T' + time_end + ':00Z')
                for l in range(len(groups)):
                    group_num = groups[l].get("name")
                    # print(group_num)
                teachers = lessons[k].get("teachers")
                if teachers is None:
                    teachers = [{"full_name": 'Тот, кого нельзя называть'}]
                for m in range(len(teachers)):
                    teacher_name = teachers[m].get("full_name")
                    # print(teacher_name)
                auditories = lessons[k].get("auditories")[0].get("building").get("name")
                # print(auditories)
                lms_url = lessons[k].get("lms_url")
                # print(lms_url)
                # записал в результат некоторое обобщение из чего состоит событие
                result = {
                    'StartTime': ftimes,
                    'EndTime': ftimee,
                    'summary': subject,
                    'description': Type + "\n" + group_num + "\n" + teacher_name + " URL:" + lms_url + "\nКомментарий: " + add_discription,
                    'location': auditories,
                }
                # print("сейчас делаем: " + str(result))
                # получаем инфу о уже существующих событиях в этом календаре, возможно поменять функцию поулчения списка
                # потому что вроже это список вообще всех событий в календаре, токен некст пейдж вроде проверяет на смену
                # так тчо это можно тоже использовать для проверки

            # if result not in exists:
                if result in exists:
                    print("Такое событие уже создано")
                else:

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
                        'description': Type + "\n" + group_num + "\n" + teacher_name + " URL:" + lms_url + "\nКомментарий: " + add_discription,
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
                        #     }]
                    }

                    maxAttendees = 5
                    sendNotification =  ntf
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
        # else:
        #     print("такое событие уже есть")
                # тут исправить,если элементы обощения текущего создаваемого события отсутствуют в списке уже существующих
                # событий, то мы создаём такое событие
                # можно попробовать проверку на соответствие собыйти сделать вот так:
                # A1 = (result['StartTime'] == exists['start']['dateTime'])
                # A2 = (result['EndTime'] == exists['end']['dateTime'])
                # A3 = (result['summary'] == exists['summary'])
                # A4 = (result['description'] == exists['description'])
                # A5 = (result['location'] == exists['location'])
                # если все эти события совпали, то создаём событие, которого нет
                # if !A1 || !A2 || !A3 || !A4 || !A5:
                # в цикле тогда делаем событие а в элсе пишем мол такое событие уже есть (этот блок можно использовать для
                # проверки на изменение расписание=я, тип если что-то изменится, для новосозданного события поменять цвет!)
                # if result[''] not in exists:
                    # page_token = None
                    # while True:
                    #     events = service.events().list(calendarId=calendar_trpo_id, pageToken=page_token).execute()
                    #     for event in events['items']:
                    #         print(event)
                    #     page_token = events.get('nextPageToken')
                    #     if not page_token:
                    #

                # event_request_body = {
                #     'start': {
                #         'dateTime': ftimes,
                #         'timeZone': 'Europe/Moscow'
                #     },
                #     'end': {
                #         'dateTime': ftimee,
                #         'timeZone': 'Europe/Moscow'
                #     },
                #     'summary': subject,
                #     'description': Type + " " + group_num + "" + teacher_name,
                #     'colorId': 5,
                #     'status': 'confirmed',
                #     'transparency': 'opaque',
                #     'visibility': 'private',
                #     'location': auditories,
                #     # 'attendees': [
                #     #     {
                #     #         'displayName': 'JJ',
                #     #         'comment': 'I enjoy coding',
                #     #         'email': 'Udovichenkop@gmail.com',
                #     #         'optional': False,
                #     #         'organizer': False,
                #     #         'responseStatus': 'accepted',
                #     #     }]
                #     }
                #
                # maxAttendees = 5
                # sendNotification = True
                # sendUpdate = 'none'
                # supportsAttachments = True
                #
                # event_response = service.events().insert(
                #     calendarId=calendar_trpo_id,
                #     maxAttendees=maxAttendees,
                #     sendNotifications=sendNotification,
                #     sendUpdates=sendUpdate,
                #     supportsAttachments=supportsAttachments,
                #     body=event_request_body
                # ).execute()
                # иначе, нужно не просто дать инфу что такое уже есть, а ещё и перейти на следующую итерацию цикла
                # а не закончить обход!!


                # добавил проерку на уже созданные события всем этим цыклом возможно надо исправлять
    return print("события на этот период созданы")


# print(event_response)

if __name__ == "__main__":
	main()
