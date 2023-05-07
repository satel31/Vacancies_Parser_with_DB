import requests


class EmployerRequest:
    """Обеспечивает запрос данных о работодателе с hh.ru"""

    def __init__(self, key_word: str) -> None:
        """Инициирует запрос ключевым словом и ссылкой"""

        self.key_word = key_word.lower()

        # Ссылка на работодателей с открытыми вакансиями
        self.__url: str = "https://api.hh.ru/employers?only_with_vacancies=true"

    def request_data(self) -> list[dict]:
        """Получает данные о работодателях с hh.ru"""

        # Параметры для запроса: количество работодателей на странице (15), регион (Россия), ключевое слово
        params: dict = {
            "per_page": 15,
            "area": 113,
            "text": self.key_word
        }

        # Осуществляем запрос
        response = requests.get(self.__url, params=params)

        if response.status_code == 200:
            employers = response.json()['items']
            return employers
        else:
            print("Error:", response.status_code)

    def get_id(self, employers: list[dict]) -> list:
        """Получает список id работодателей"""

        id_list = []
        for id in employers:
            id_list.append(id['id'])
        return id_list


class VacancyRequest:
    """Обеспечивает запрос данных о вакансиях работодателей с hh.ru"""

    def __init__(self, employer_ids: list) -> None:
        """Инициирует запрос ключевым словом и ссылкой"""

        self.employer_ids = employer_ids

        # Ссылка на вакансии
        self.__url: str = "https://api.hh.ru/vacancies"

    def request_data(self, page: int = 0) -> dict:
        """Получает данные о вакансиях с hh.ru"""

        # Параметры для запроса: id работодателей, количество вакансий на странице (100), страница
        params: dict = {
            "employer_id": self.employer_ids,
            "per_page": 100,
            "page": page
        }

        # Осуществляем запрос
        response = requests.get(self.__url, params=params)

        if response.status_code == 200:
            vacancies = response.json()
            return vacancies
        else:
            print("Error:", response.status_code)

    def pass_by_page(self) -> list[dict]:
        """Получаем данные постранично"""

        data: dict = self.request_data()
        pages: int = data['pages']
        all_vacancies = []
        for p in range(pages):
            data_by_page = self.request_data(p)
            for vacancy in data_by_page['items']:
                all_vacancies.append(vacancy)
        return all_vacancies
