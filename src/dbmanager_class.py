import psycopg2


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
        """При инициализации объекта создаётся соединение, курсор"""
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        conn = psycopg2.connect(host=self.host, dbname='postgres', user=self.user, password=self.password,
                                port=self.port)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {self.dbname}")
        cur.execute(f"CREATE DATABASE {self.dbname}")

        conn.close()

        # Создаем соединение
        self.conn = psycopg2.connect(host=host, database=dbname, user=user, password=password, port=port)
        # Создаем курсор
        self.cur = self.conn.cursor()
        # Создаем автокоммит
        self.conn.autocommit = True



class EmployersDB(DBManager):
    """Обеспечивает взаимодействие с базой данных Postgres"""

    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
        """При инициализации объекта создаётся соединение, курсор"""
        super().__init__(dbname, user, password, host, port)

        # Создаем соединение
        self.conn = psycopg2.connect(host=self.host, database=self.dbname, user=self.user, password=self.password,
                                     port=self.port)
        # Создаем курсор
        self.cur = self.conn.cursor()
        # Создаем автокоммит
        self.conn.autocommit = True

    def create_table_employer(self) -> None:
        """Создаём таблицу в БД"""
        with self.conn:
            self.cur.execute(f"""
                CREATE TABLE employers (
                    company_id INTEGER PRIMARY KEY,
                    company_name VARCHAR(100) NOT NULL,
                    company_url TEXT,
                    vacancies_url TEXT,
                    amount_of_vacancies INTEGER,
                    repository_url TEXT
                )
            """)

    def insert_data_to_db(self, employers: list[dict]) -> None:
        """Добавляем данные в таблицу в БД"""
        with self.conn:
            for employer in employers:
                self.cur.execute(
                    f"""
                        INSERT INTO employers (company_id, company_name, company_url, vacancies_url, amount_of_vacancies, 
                                               repository_url
                                               )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                    (employer['company_id'], employer['company_name'], employer['company_url'],
                     employer['vacancies_url'], employer['amount_of_vacancies'], employer['repository_url'])
                )


class VacanciesDB(DBManager):
    """Обеспечивает взаимодействие с базой данных Postgres"""

    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
        """При инициализации объекта создаётся соединение, курсор"""

        super().__init__(dbname, user, password, host, port)

        # Создаем соединение
        self.conn = psycopg2.connect(host=self.host, database=self.dbname, user=self.user, password=self.password,
                                     port=self.port)
        # Создаем курсор
        self.cur = self.conn.cursor()
        # Создаем автокоммит
        self.conn.autocommit = True

    def create_table_vacancies(self) -> None:
        """Создаём таблицу в БД"""
        with self.conn:
            self.cur.execute(f"""
                    CREATE TABLE vacancies (
                        vacancy_id INTEGER PRIMARY KEY,
                        vacancy_name VARCHAR(100) NOT NULL,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        currency VARCHAR(100),
                        requirements TEXT,
                        responsibilities TEXT,
                        has_test BOOL,
                        employment VARCHAR(100),
                        company_id INTEGER NOT NULL,
                        company_name VARCHAR(100) NOT NULL,
                        city VARCHAR(100),
                        address TEXT
                    )
                """)
            self.cur.execute(f"""
                ALTER TABLE vacancies 
                ADD CONSTRAINT fk_vacancies_employers
                FOREIGN KEY (company_id) REFERENCES employer(company_id)
                """)

    def insert_data_to_db(self, vacancies: list[dict]) -> None:
        """Добавляем данные в таблицу в БД"""
        with self.conn:
            for vacancy in vacancies:
                self.cur.execute(
                    f"""
                        INSERT INTO vacancies (vacancy_id, vacancy_name, salary_from, salary_to, currency, requirements,
                                               responsibilities, has_test, employment, company_id, company_name, city,
                                               address
                                               )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                    (vacancies['vacancy_id'], vacancies['vacancy_name'], vacancies['salary_from'],
                     vacancies['salary_to'], vacancies['currency'], vacancies['requirements'],
                     vacancies['responsibilities'], vacancies['has_test'], vacancies['employment'], vacancies['company_id'],
                     vacancies['company_name'], vacancies['city'], vacancies['address'])
                )





def insert_data_to_json(self) -> None:
    """Считываем данные из БД и экспортируем в файл JSON"""
    # Задаём название файла по названию таблицы
    file = f'{self.table_name}.json'
    # Считываем данные из БД
    repos_dict: list[dict] = self.read_db()
    # Записываем данные в файл
    with open(file, 'a', encoding='utf-8') as f:
        json.dump(repos_dict, f, ensure_ascii=False)


def read_db(self, sort_by: str = None, limit: int = None) -> list[dict]:
    """Получаем и возвращаем данные из таблицы с сортировкой и/или ограничением или без"""
    with self.conn:
        # Данные с сортировкой и ограничением
        if sort_by and limit:
            self.cur.execute(f"""SELECT * FROM {self.table_name} ORDER BY {sort_by} LIMIT {limit}""")
        # Данные только с сортировкой
        elif sort_by:
            self.cur.execute(f"""SELECT * FROM {self.table_name} ORDER BY {sort_by}""")
        # Данные только с ограничением
        elif limit:
            self.cur.execute(f"""SELECT * FROM {self.table_name} LIMIT {limit}""")
        # Все данные без сортировки
        else:
            self.cur.execute(f"""SELECT * FROM {self.table_name}""")
        repos_data: list[tuple] = self.cur.fetchall()
        repos_dict = []
        # Преобразуем данные в список словарей репозиториев
        for data in repos_data:
            repos_dict.append({'repository_id': data[0],
                               'title': data[1],
                               'owner': data[2],
                               'forks': data[3],
                               'language': data[4],
                               'repository_url': data[5]
                               })
    return repos_dict
