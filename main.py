from src.db_manager import DBManager
from src.hh import HH

def main():
   print('Приветствую Вас! Сейчас мы поработаем с вакансиями сайта hh.ru!')
   my_db = DBManager('vacancies')
   print('Сoздаем базу данных и таблицы')
   print()
   my_db.create_database()
   print('База данных создана.')
   print()
   data_hh= HH()
   employers = data_hh.get_data_vacancies()
   my_db.insert(employers)
   print('Вакансии успешно загружены!')


   print('Выберите цифру из предложенного меню:')
   print(f"""
  1. Получить список всех компаний и количество вакансий у каждой компании
  2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
  3. Получить среднюю зарплату по вакансиям
  4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
  5. получает список всех вакансий, в названии которых содержится ключевое слово
  0. Выход из программы""")
   print()
   while True:
      user_input = input('Введите цифру: ')
      if user_input == '1':
         my_db.get_companies_and_vacancies_count()
      elif user_input == '2':
         my_db.get_all_vacancies()
      elif user_input == '3':
         my_db.get_avg_salary()
      elif user_input == '4':
         my_db.get_vacancies_with_higher_salary()
      elif user_input == '5':
         user_keyword = input('Введите слово: ')
         my_db.get_vacancies_with_keyword(user_keyword)
      elif user_input == '0':
         break
      else:
         print('Некорректный ввод')


if __name__ == '__main__':
   main()



