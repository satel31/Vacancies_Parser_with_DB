from src.db_manager_class import DBManager

def user_interaction(dbmanager):
    """Запрашивает у пользователя действие, повторяется до тех пор, пока пользователей не введёт 'нет' """

    # Перечень возможных действий
    print('Теперь Вы можете:\n'
          '1) Увидеть список всех компаний и количество вакансий у каждой компании\n'
          '2) Увидеть список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию\n'
          '3) Увидеть среднюю зарплату по вакансиям\n'
          '4) Увидеть список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
          '5) Увидеть список всех вакансий, в названии которых содержатся ключевые слова\n'
          '6) Увидеть все данные в таблице\n')

    # Запрос действия у пользователя
    user_action: str = input('Введите номер действия без скобки')

    # Выполнение действий
    if user_action == '1':
        result = dbmanager.get_companies_and_vacancies_count()
        for item in result:
            print(*item, sep=', ')

    elif user_action == '2':
        result = dbmanager.get_all_vacancies()
        for item in result:
            print(*item, sep=', ')

    elif user_action == '3':
        result = dbmanager.get_avg_salary()
        print(round(*result, 2))

    elif user_action == '4':
        result = dbmanager.get_vacancies_with_higher_salary()
        for item in result:
            print(*item, sep=', ')

    elif user_action == '5':
        print('Введите ключевое слово для поиска')
        keyword = input()
        result = dbmanager.get_vacancies_with_keyword(keyword)
        for item in result:
            print(*item, sep=', ')

    elif user_action == '6':
        print('Данные из какой таблице вывести: employers или vacancies?')
        tablename = input()
        if tablename == 'employers' or tablename == 'vacancies':
            result = dbmanager.read_db(tablename)
            for item in result:
                print(*item, sep=', ')
        else:
            print('Такой таблицы нет. Попробуйте снова')

