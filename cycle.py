
from datetime import date
import pandas as pd
from pathlib import Path


def main():
    answers = 2
    urls = get_weeks(answers)
    print(urls)


def get_weeks(answers):
    path_i = Path('task.txt')
    task = open(path_i, 'r', encoding='utf-8')
    answers = (task.read()).split('\n')
    start_date = answers[3]
    # print('insert start date as YYYY-MM-DD')
    # start_date = input()
    start_days = int(start_date[8:])
    start_months = int(start_date[5:7])
    start_years = int(start_date[0:4])
    # print('insert finish date as YYYY-MM-DD')
    finish_date = answers[4]
    finish_days = int(finish_date[8:])
    finish_months = int(finish_date[5:7])
    finish_years = int(finish_date[0:4])
    midday=pd.to_datetime(start_date)
    if start_days < 13:
        n = 28 - start_days
        new_start_date = str(start_days + n) + start_date[2:]
        midday = pd.to_datetime(new_start_date) - pd.DateOffset(days=n)
    d0 = date(finish_years, finish_months, finish_days)
    d1 = date(start_years, start_months, start_days)
    difference = d0 - d1
    amountofdays = str(difference)
    amount = amountofdays.split()
    spisok = []
    for i in range(int(amount[0]) // 7 + 1):
        spisok.append(str(midday)[0:10])
        midday = pd.to_datetime(midday) + pd.DateOffset(days=7)

    return spisok

if __name__ == "__main__":
	main()
