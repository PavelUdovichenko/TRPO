import requests
from datetime import datetime
import ast
from pathlib import Path
import cycle
import json

def main():
    url = get_url()
    TimetableForPeriod = get_content(url)
    print(TimetableForPeriod)



def get_content(url):
    fin_content = []
    for i in range(len(url)):
        url_response = requests.get(url[i])
        content = json.loads(url_response.text)
        fin_content.append(content)
    print(fin_content)
    return fin_content

def get_url():

    # date = ['2021-12-27', '2022-01-03', '2022-01-10', '2022-01-17', '2022-01-24', '2022-01-31']
    path_i=Path('task.txt')
    # print(date)
    # current_date = datetime.now().date()
    task = open(path_i, 'r', encoding='utf-8')
    answers = (task.read()).split('\n')
    date = cycle.get_weeks(answers)
    # decision = answers[0]
    if answers[0].lower()=='student':
        faculties_url='https://ruz.spbstu.ru/api/v1/ruz/faculties'
        fac_res=requests.get(faculties_url)
        dict_con_fuc = ast.literal_eval(fac_res.text)
        fucabbr = str(answers[2])
        fac_id = 0
        for abbr in dict_con_fuc['faculties']:
            if abbr['abbr'] == fucabbr:
                fac_id=abbr['id']
        group_id=0
        groupslink1='https://ruz.spbstu.ru/api/v1/ruz/faculties/'
        groupslink2='/groups'
        if fac_id!=0:
            groupslink = groupslink1 + str(fac_id) + groupslink2
        else:
            print('Проверьте номер группы')
            exit(0)
        group_res = requests.get(groupslink)
        dict_con_group = ast.literal_eval(group_res.text)
        group=str(answers[1])
        for group_name in dict_con_group['groups']:
            if group_name['name']== group:
                group_id = group_name['id']
        #print(group_id)
        urls = []
        url3 = 'https://ruz.spbstu.ru/api/v1/ruz/scheduler/'
        if fac_id != 0:
            for i in range(len(date)):
                url_api= url3 + str(group_id) + str('?date=') + str(date[i])
                urls.append(url_api)
            # print(urls)
            return urls
        else:
            print('Проверьте номер группы')
            exit(0)
    if answers[0].lower()=='teacher':
        teachers_url = 'https://ruz.spbstu.ru/api/v1/ruz/teachers/'
        teachers_res = requests.get(teachers_url)
        dict_con_teachers = ast.literal_eval(teachers_res.text)
        print('Введите Фамилию Имя Отчество')
        Tname=str(input())
        teacher_id=0
        # url_t = []
        for teacher_name in dict_con_teachers['teachers']:
            if teacher_name['full_name'] == Tname:
               teacher_id = teacher_name['id']
            elif teacher_name['first_name'] == Tname:
               teacher_id = teacher_name['id']
        url3 = 'https://ruz.spbstu.ru/api/v1/ruz/teachers/'
        urls = []
        if teacher_id != 0:
            for i in range(len(date)):
                url_t = url3 + str(teacher_id) + str('/scheduler?date=') + str(date[i])
                urls.append(url_t)
            return urls
        else:
            print('Проверьте написание ФИО')
            exit(0)
    else:
            exit(0)
    print("вот")


if __name__ == "__main__":
    main()


