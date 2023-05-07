import os

from dotenv import load_dotenv

import psycopg2

from src.requests_classes import EmployerRequest, VacancyRequest
from src.functions import employer_data_db, vacancy_data_db
from src.db_manager_class import DBManager, EmployersDB, VacanciesDB
from src.user_interaction import user_interaction


def main() -> None:
    """Основной интерфейс программы"""

    # Запрашиваем имя пользователя для поиска
    print('Введите ключевое слово для поиска работодателей')
    emp_keyword: str = input()

    # Собираем статистику по репозиториям пользователя
    er = EmployerRequest(emp_keyword)
    employers = er.request_data()
    employer_ids = er.get_id(employers)

    vr = VacancyRequest(employer_ids)
    vacancies = vr.pass_by_page()

    employers_data = employer_data_db(employers)
    vacancies_data = vacancy_data_db(vacancies)

    # Запрашиваем имя таблицы
    print('Введите имя базы данных')
    db_name: str = input()

    # Загружаем данные для подключения к БД из локального файла env
    load_dotenv()

    db_config = {
        'user': os.getenv('user'),
        'password': os.getenv('password'),
        'host': os.getenv('host'),
        'port': os.getenv('port'),
    }

    conn = psycopg2.connect(**db_config, dbname='test')
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()

    # Создаем экземпляр PostgresDB, при инициализации которого создаётся таблица
    db = DBManager(dbname=db_name, **db_config)
    # Сохраняем данные в БД
    emp_db = EmployersDB(dbname=db_name, **db_config)
    emp_db.insert_data_to_db(employers_data)

    vac_db = VacanciesDB(dbname=db_name, **db_config)
    vac_db.insert_data_to_db(vacancies_data)

    print(f'Данные успешно записаны в базу данных {db_name} в таблицы employers и vacancies')

    user_action = input('Вы хотите продолжить? Введите да/нет ')

    while user_action.lower() == 'да':
        user_interaction(db)
        user_action = input('Вы хотите продолжить? Введите да/нет ')




if __name__ == '__main__':
    main()
