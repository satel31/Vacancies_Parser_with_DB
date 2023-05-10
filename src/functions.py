import psycopg2
def employer_data_db(employer_data: list[dict]) -> list[dict]:
    """Составляем словари с нужными данными для внесения в БД в таблицу employer"""
    employer_db = []
    for emp in employer_data:
        employer = {'company_id': emp['id'],
                    'company_name': emp['name'],
                    'company_url': emp['alternate_url'],
                    'vacancies_url': emp['vacancies_url'],
                    'amount_of_vacancies': emp['open_vacancies']
                    }
        employer_db.append(employer)
    return employer_db


def vacancy_data_db(vacancy_data: list[dict]) -> list[dict]:
    """Составляем словари с нужными данными для внесения в БД в таблицу vacancy"""
    vacancy_db = []
    for vac in vacancy_data:
        vacancy = {'vacancy_id': vac['id'],
                   'vacancy_name': vac['name'],
                   'vacancy_url': vac['alternate_url'],
                   'salary_from': None,
                   'salary_to': None,
                   'currency': None,
                   'requirements': vac['snippet']['requirement'],
                   'responsibilities': vac['snippet']['responsibility'],
                   'has_test': vac['has_test'],
                   'employment': vac['employment']['name'],
                   'company_id': None,
                   'company_name': vac['employer']['name'],
                   'city': vac['area']['name'],
                   'address': None
                   }
        try:
            vacancy['salary_from'] = vac['salary']['from']
            vacancy['salary_to'] = vac['salary']['to']
            vacancy['currency'] = vac['salary']['currency']
            vacancy['address'] = vac['address']['raw']
            vacancy['company_id'] = vac['employer']['id'],
        except TypeError:
            pass

        vacancy_db.append(vacancy)

    return vacancy_db


def create_db(dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432'):
    """Создаём новую базу данных"""

    # Подключаемся к БД test
    conn = psycopg2.connect(host=host, user=user, password=password, port=port, dbname='test')
    conn.autocommit = True
    cur = conn.cursor()

    # Удаляем БД, если имя совпадает
    cur.execute(f"DROP DATABASE {dbname}")
    # Создаём новую БД
    cur.execute(f"CREATE DATABASE {dbname}")

    conn.close()
