--Создает таблицу вакансий
CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                title varchar(100) NOT NULL ,
                salary_min REAL,
                salary_max REAL,
                employer_id INT REFERENCES employers(employer_id) NOT NULL,
                vacancy_url TEXT);

--Сoздает таблицу компаний-работадателей
CREATE TABLE employers (employer_id INT PRIMARY KEY, employer_name varchar NOT NULL

--Получает список всех компаний и количество вакансий у каждой компании
SELECT employer_name, COUNT(*) AS number_of_vacancies
FROM vacancies
LEFT JOIN employers USING(employer_id)
GROUP BY employer_name
ORDER BY number_of_vacancies DESC, employer_name

--Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT employers.employer_name, title, salary_min, salary_max, vacancy_url
FROM vacancies
JOIN employers USING(employer_id)
WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL
ORDER BY salary_min DESC, title

--Получает среднюю зарплату по вакансиям
SELECT ROUND(AVG(salary_min + salary_max/2)) AS average_salary
FROM vacancies

--Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT title, (salary_min + salary_max/2) AS salary
FROM vacancies
WHERE (salary_min + salary_max/2) > (SELECT AVG((salary_min + salary_max/2)) FROM vacancies)
ORDER BY (salary_min + salary_max/2) DESC, title


-- Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
SELECT title, salary_min, salary_max, vacancy_url
FROM vacancies
WHERE lower(title) LIKE lower(%s);

