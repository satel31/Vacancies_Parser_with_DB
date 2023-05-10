import os

from dotenv import load_dotenv

import psycopg2

from src.requests_classes import EmployerRequest, VacancyRequest
from src.functions import employer_data_db, vacancy_data_db, create_db
from src.db_manager_class import DBManager, EmployersDB, VacanciesDB
from src.user_interaction import user_interaction


def main() -> None:
    """Основной интерфейс программы"""

    # Запрашиваем ключевое слово для поиска
    print('Введите ключевое слово/слова для поиска работодателей. Несколько слов вводите через запятую и пробел')
    emp_keyword: str = input().split(', ')

    # Собираем данные по работодателям
    er = EmployerRequest(emp_keyword)
    employers: list[dict] = er.request_data()

    # Получаем данные об id работодателей
    employer_ids: list = er.get_id(employers)

    # Собираем данные по вакансиям работодателей
    vr = VacancyRequest(employer_ids)
    vacancies: list[dict] = vr.pass_by_page()

    # Преобразуем данные для внесения в БД
    employers_data: list[dict] = employer_data_db(employers)
    vacancies_data: list[dict] = vacancy_data_db(vacancies)

    if len(employers_data) == 0:
        print("Работодателей по Вашему запросу не найдено. Попробуйте ещё раз с иным ключевым словом")
        return

    # Запрашиваем имя базы данных
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

    # Создаем новую БД
    create_db(dbname=db_name, **db_config)

    # Создаем экземпляр DBManager, при инициализации которого создаётся подключение к новой БД
    db = DBManager(dbname=db_name, **db_config)

    # Сохраняем данные в БД в таблицу employers
    emp_db = EmployersDB(dbname=db_name, **db_config)
    emp_db.insert_data_to_db(employers_data)

    # Сохраняем данные в БД в таблицу vacancies
    vac_db = VacanciesDB(dbname=db_name, **db_config)
    vac_db.insert_data_to_db(vacancies_data)

    print(f'Данные успешно записаны в базу данных {db_name} в таблицы employers и vacancies')

    # Запрашиваем у пользователя желание продолжить
    user_action = input('Вы хотите продолжить? Введите да/нет ')

    # Работаем с БД пока пользователь не введёт 'нет'
    while user_action.lower() == 'да':
        user_interaction(db)
        user_action = input('Вы хотите продолжить? Введите да/нет ')


if __name__ == '__main__':
    main()
