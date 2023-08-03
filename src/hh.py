import requests
from src.employers import employers_list
import time

class HH:
    '''
    Класс для работы с ресурсом HeadHanter.ru
    '''

    def __init__(self):
        self.api_url = 'https://api.hh.ru/vacancies'
        self.keyword = None
        self.per_page = 100

    def get_data_vacancies(self):
        '''
        Метод для получения данных о вакансиях с помощью ApiHH
        '''

        data_vacancies = []

        for employer_id in employers_list:
            params = {
                'employer_id': employer_id,
                "per_page": self.per_page,
                'area': 113

            }

            hh_response = requests.get(self.api_url, params)
            if hh_response.status_code == 200:
                data = hh_response.json()
                data_vacancies.append(data)
                time.sleep(0.20)  # Задержка запроса
                #print(data_vacancies)


            else:
                print(f'Ошибка подключения к серверу - {hh_response.status_code}')

        return data_vacancies





#hh = HH()
#print(hh.get_data_vacancies())
#print(len(hh.get_data_vacancies()))