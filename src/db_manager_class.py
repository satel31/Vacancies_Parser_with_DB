import psycopg2


class DBManager:
    """Обеспечивает взаимодействие с базой данных"""
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
        """При инициализации объекта создаётся соединение и курсор"""

        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # Создаем соединение
        self.conn = psycopg2.connect(host=host, database=dbname, user=user, password=password, port=port)
        # Создаем курсор
        self.cur = self.conn.cursor()
        # Создаем автокоммит
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Возвращает список всех компаний и количество вакансий у каждой компании"""
        with self.conn:
            self.cur.execute(f"""SELECT company_name, amount_of_vacancies FROM employers""")
            empl_and_vac_count = self.cur.fetchall()
            return empl_and_vac_count

    def get_all_vacancies(self) -> list[tuple]:
        """Возвращает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn:
            self.cur.execute(f"""SELECT company_name, vacancy_name,  salary_from, salary_to, currency, vacancy_url
                                 FROM vacancies
                                 """)
            all_vacancies = self.cur.fetchall()
            return all_vacancies

    def get_avg_salary(self) -> tuple:
        """Возвращает среднюю зарплату по вакансиям на основе нижней и верхней границ"""
        with self.conn:
            self.cur.execute(f"""SELECT (AVG(salary_from) + AVG(salary_to)) / 2 AS average_salary FROM vacancies""")
            avg_salary = self.cur.fetchone()
            return avg_salary

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn:
            self.cur.execute(f"""SELECT * FROM vacancies 
                                 WHERE salary_from > (SELECT (AVG(salary_from) + AVG(salary_to)) / 2 FROM vacancies) 
                                 OR salary_to > (SELECT (AVG(salary_from) + AVG(salary_to)) / 2 FROM vacancies)
                                 """)
            higher_salary = self.cur.fetchall()
            return higher_salary

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Возвращает список всех вакансий, в названии которых содержится ключевое слово"""
        with self.conn:
            self.cur.execute(f"""SELECT * FROM vacancies 
                                 WHERE vacancy_name LIKE '%{keyword}%'
                                 """)
            vac_w_kw = self.cur.fetchall()
            return vac_w_kw

    def read_db(self, table_name: str) -> list[tuple]:
        """Получаем и возвращаем все данные из таблицы"""
        with self.conn:
            self.cur.execute(f"""SELECT * FROM {table_name}""")
            result = self.cur.fetchall()
            return result


class EmployersDB(DBManager):
    """Обеспечивает взаимодействие с таблицей employers"""

    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
        """При инициализации объекта создаётся соединение и курсор"""
        super().__init__(dbname, user, password, host, port)

        self.create_table_employer()

    def create_table_employer(self) -> None:
        """Создаём таблицу в БД"""
        with self.conn:
            self.cur.execute(f"""
                CREATE TABLE employers (
                    company_id INTEGER PRIMARY KEY,
                    company_name VARCHAR(100) NOT NULL,
                    company_url TEXT,
                    vacancies_url TEXT,
                    amount_of_vacancies INTEGER
                )
            """)

    def insert_data_to_db(self, employers: list[dict]) -> None:
        """Добавляем данные в таблицу в БД"""
        with self.conn:
            for employer in employers:
                self.cur.execute(
                    f"""
                        INSERT INTO employers (company_id, company_name, company_url, vacancies_url, amount_of_vacancies
                                               )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                    (employer['company_id'], employer['company_name'], employer['company_url'],
                     employer['vacancies_url'], employer['amount_of_vacancies'])
                )


class VacanciesDB(DBManager):
    """Обеспечивает взаимодействие с таблицей vacancies"""

    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
        """При инициализации объекта создаётся соединение, курсор"""

        super().__init__(dbname, user, password, host, port)

        self.create_table_vacancies()

    def create_table_vacancies(self) -> None:
        """Создаём таблицу vacancies в БД"""
        with self.conn:
            self.cur.execute(f"""
                    CREATE TABLE vacancies (
                        vacancy_id INTEGER PRIMARY KEY,
                        vacancy_name VARCHAR(100) NOT NULL,
                        vacancy_url TEXT,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        currency VARCHAR(100),
                        requirements TEXT,
                        responsibilities TEXT,
                        has_test BOOL,
                        employment VARCHAR(100),
                        company_id INTEGER,
                        company_name VARCHAR(100) NOT NULL,
                        city VARCHAR(100),
                        address TEXT
                    )
                """)
            self.cur.execute(f"""
                ALTER TABLE vacancies 
                ADD CONSTRAINT fk_vacancies_employers
                FOREIGN KEY (company_id) REFERENCES employers(company_id)
                """)

    def insert_data_to_db(self, vacancies: list[dict]) -> None:
        """Добавляем данные в таблицу vacancies в БД"""
        with self.conn:
            for vacancy in vacancies:
                self.cur.execute(
                    f"""
                        INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_url, salary_from, salary_to, currency, requirements,
                                               responsibilities, has_test, employment, company_id, company_name, city,
                                               address
                                               )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                    (vacancy['vacancy_id'], vacancy['vacancy_name'], vacancy['vacancy_url'], vacancy['salary_from'],
                     vacancy['salary_to'], vacancy['currency'], vacancy['requirements'],
                     vacancy['responsibilities'], vacancy['has_test'], vacancy['employment'], vacancy['company_id'],
                     vacancy['company_name'], vacancy['city'], vacancy['address'])
                )
