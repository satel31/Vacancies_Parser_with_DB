import requests


class EmployerRequest:
    """Class for getting employer data from hh.ru"""

    def __init__(self, key_word: str) -> None:
        """Initialize the request with parameters of request and url"""

        self.key_word: str = key_word.lower()

        self.__url: str = "https://api.hh.ru/employers?only_with_vacancies=true"

    def request_data(self) -> list[dict]:
        """Get employer data from hh.ru"""

        params: dict = {
            "per_page": 15,
            "area": 113,
            "text": self.key_word
        }
        response = requests.get(self.__url, params=params)

        if response.status_code == 200:
            employers = response.json()['items']
            return employers
        else:
            print("Error:", response.status_code)

    def get_id(self, employers):
        id_list = []
        for id in employers:
            id_list.append(id['id'])
        return id_list


class VacancyRequest:
    """Class for getting vacancy data by employer's id from hh.ru"""

    def __init__(self, employer_ids) -> None:
        """Initialize the request with employer's ids and url"""

        self.employer_ids = employer_ids
        self.__url: str = "https://api.hh.ru/vacancies"

    def request_data(self, page: int = 0) -> dict:
        """Get data from hh.ru"""

        params: dict = {
            "employer_id": self.employer_ids,
            "per_page": 100,
            "page": page
        }

        response = requests.get(self.__url, params=params)

        if response.status_code == 200:
            vacancies = response.json()
            return vacancies
        else:
            print("Error:", response.status_code)

    def pass_by_page(self) -> None:
        """Pass data page by page"""

        data: dict = self.request_data()
        pages: int = data['pages']
        all_vacancies = []
        for p in range(pages):
            data_by_page = self.request_data(p)
            for vacancy in data_by_page['items']:
                all_vacancies.append(vacancy)
        return all_vacancies
