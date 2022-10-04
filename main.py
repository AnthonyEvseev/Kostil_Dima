import requests
import time
import random
from datetime import datetime
import pandas as pd
import seaborn as sns

import warnings

sns.set(rc={'figure.figsize': (12, 7)})


headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}


def get_data_from_hh(url):
    data = requests.get(url, headers=headers, timeout=5).json()
    return data


def prepare_salary(data):
    salary_from = []
    salary_to = []
    print('Количество вакансий: ', data['found'])

    quantity_pagination = round(data['found'] / 100, 0) + 1
    page = 0

    while page <= quantity_pagination:
        url = f'https://api.hh.ru/vacancies?clusters=true&only_with_salary=true&enable_snippets=true&st=searchVacancy&' \
              f'text=менеджер+по+работе+с+клиентами&search_field=name&per_page=100&page={page}&area=64'
        data = get_data_from_hh(url)

        for vacancy in data['items']:

            print(vacancy['name'], '->', vacancy['published_at'][:10], '->', vacancy['salary']['from'], '->',
                  vacancy['salary']['to'])

            if type(vacancy['salary']['from']) == int:
                salary_from.append(vacancy['salary']['from'])
            if type(vacancy['salary']['to']) == int:
                salary_to.append(vacancy['salary']['to'])

        page += 1
        random_timeout = random.randint(3, 9)
        time.sleep(random_timeout)

    salary = {
        'salary_from': salary_from,
        'salary_to': salary_to
    }

    return salary


def salary_average(salary):
    salary_from_avg = round(sum(salary['salary_from']) / len(salary['salary_from']), 0)
    salary_to_avg = round(sum(salary['salary_to']) / len(salary['salary_to']), 0)

    salary_avg = {
        'salary_from_avg': salary_from_avg,
        'salary_to_avg': salary_to_avg
    }

    return salary_avg


def seaborn_displot(data):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d-%H%M%S")
    filename = 'raspredelenie_' + date + '.png'

    pd_data = pd.Series(data)
    res = sns.displot(pd_data)
    res.savefig(filename)


def seaborn_boxplot(data):
    warnings.simplefilter(action="ignore", category=FutureWarning)
    now = datetime.now()
    date = now.strftime("%Y-%m-%d-%H%M%S")
    filename = 'raspredelenie_box_' + date + '.png'

    pd_data = pd.Series(data)
    data_result = pd_data.value_counts().sort_values(ascending=False).index.values
    sns.boxplot(data_result).figure.savefig(filename)


url = 'https://api.hh.ru/vacancies?clusters=true&only_with_salary=true&enable_snippets=true&st=searchVacancy' \
      '&text=менеджер+по+работе+с+клиентами&search_field=name&per_page=100&area=64'

data = get_data_from_hh(url)
salary = prepare_salary(data)
salary_avg = salary_average(salary)
