import psycopg2
from config import config


class DBManager:
    """Класс для работы с базой данных, инициализируется названием базы данных и данными из конфигурационного файла"""
    def __init__(self, dbname: str):
        self.dbname = dbname
        self.params = config()


    def create_database(self):
        """Создает базу данных и таблицы"""
        # Подключаемся к postgres, чтобы создать БД
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()


        cur.execute(f"DROP DATABASE IF EXISTS {self.dbname}")
        cur.execute(f"CREATE DATABASE {self.dbname}")

        cur.close()
        conn.close()

        # Подключаемся к созданной БД и создаем таблицы
        conn = psycopg2.connect(dbname=self.dbname, **self.params)

        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE employers (employer_id INT PRIMARY KEY, employer_name varchar NOT NULL )''')

        conn.commit()

        with conn.cursor() as cur:
            cur.execute(
                '''CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY, 
                title varchar(100) NOT NULL ,
                salary_min REAL,
                salary_max REAL,
                employer_id INT REFERENCES employers(employer_id) NOT NULL,
                vacancy_url TEXT                
                )'''
            )

        conn.commit()

        conn.close()

    def insert(self, data) -> None:
        """Добавление данных в базу данных в таблицы"""
        conn = psycopg2.connect(dbname=self.dbname, **self.params)

        with conn.cursor() as cur:

            # Заполняем данными таблицу компаний-работадателей

            for emp in data:
                employer_id = emp['items'][0]['employer']['id']
                employer_name = emp['items'][0]['employer']['name']

                cur.execute(
                    """
                    INSERT INTO employers (employer_id, employer_name)
                    VALUES (%s, %s)
                    RETURNING employer_id
                    """,
                    (employer_id, employer_name)
                )
            #Заполняем данными таблицу вакансий

            for vacancy in emp['items']:

                vacancy_name = vacancy['name']

                if vacancy['salary'] is None:
                    salary_from = None
                    salary_to = None

                elif not vacancy['salary']['from']:
                    salary_from = None
                    salary_to = vacancy['salary']['to']

                elif not vacancy['salary']['to']:
                    salary_from = vacancy['salary']['from']
                    salary_to = salary_from

                else:
                    salary_from = vacancy['salary']['from']
                    salary_to = vacancy['salary']['to']

                vacancy_url = vacancy['alternate_url']

                cur.execute(
                    '''
                    INSERT INTO vacancies (title, salary_min, salary_max, employer_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ''',
                    (vacancy_name, salary_from, salary_to, employer_id, vacancy_url)
                )

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self):
        '''Получает список всех компаний и количество вакансий у каждой компании'''

        conn = psycopg2.connect(dbname=self.dbname, **self.params)

        query = """
            SELECT employer_name, COUNT(*) AS number_of_vacancies
            FROM vacancies
            LEFT JOIN employers USING(employer_id)
            GROUP BY employer_name
            ORDER BY number_of_vacancies DESC, employer_name;
           """

        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        for employers, vacancies_count in results:
            print(f"Company: {employers}, vacancies count: {vacancies_count}")

        conn.commit()
        cursor.close()
        conn.close()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """

        conn = psycopg2.connect(dbname=self.dbname, **self.params)

        query = """
            SELECT employers.employer_name, title, salary_min, salary_max, vacancy_url
            FROM vacancies
            JOIN employers USING(employer_id)
            WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL
            ORDER BY salary_min DESC, title;
            """
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        for data in results:
            print(
                f'employer_name: {data[0]}, title: {data[1]}, salary_min: {data[2]}, '
                f'salary_max: {data[3]}, vacancy_url: {data[4]}')

        conn.commit()
        cursor.close()
        conn.close()

    def get_avg_salary(self):
        '''
        Получает среднюю зарплату по вакансиям
        '''
        conn = psycopg2.connect(dbname=self.dbname, **self.params)

        query = """
            SELECT ROUND(AVG(salary_min + salary_max/2)) AS average_salary
            FROM vacancies;
            """
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        for data in results:
            print(f'average_salary: {data[0]}')

        conn.commit()
        cursor.close()
        conn.close()


    def get_vacancies_with_higher_salary(self):
        '''
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        '''

        conn = psycopg2.connect(dbname=self.dbname, **self.params)

        query = """
            SELECT title, (salary_min + salary_max/2) AS salary
            FROM vacancies
            WHERE (salary_min + salary_max/2) > (SELECT AVG((salary_min + salary_max/2)) FROM vacancies)
            ORDER BY (salary_min + salary_max/2) DESC, title;
            """

        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        for data in results:
            print(f'title: {data[0]}, salary: {data[1]}')

        conn.commit()
        cursor.close()
        conn.close()

    def get_vacancies_with_keyword(self, keyword):
        '''
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
        '''

        conn = psycopg2.connect(dbname=self.dbname, **self.params)


        query = """
        SELECT title, salary_min, salary_max, vacancy_url
        FROM vacancies
        WHERE lower(title) LIKE lower(%s);
        """
        user_keyword = f"%{keyword}%"

        with conn.cursor() as cursor:
            cursor.execute(query, (user_keyword,))
            results = cursor.fetchall()

        if len(results) == 0:
            print("По вашему запросу ничего не найдено(")
        else:
            for data in results:
                print(f'title: {data[0]}, salary_min: {data[1]}, salary_max: {data[2]}, vacancy_url: {data[3]}')

        conn.commit()
        cursor.close()
        conn.close()


