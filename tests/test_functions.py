import pytest
from src.functions import employer_data_db, vacancy_data_db


def test_employer_data_db():
    data = [{"id": "36227", "name": "000 МАГАЗИН МАГАЗИНОВ - Эксперт по торговой недвижимости",
             "url": "https://api.hh.ru/employers/36227", "alternate_url": "https://hh.ru/employer/36227",
             "logo_urls": {"original": "https://hhcdn.ru/employer-logo-original/494504.png",
                           "240": "https://hhcdn.ru/employer-logo/2419770.png",
                           "90": "https://hhcdn.ru/employer-logo/2419769.png"},
             "vacancies_url": "https://api.hh.ru/vacancies?employer_id=36227", "open_vacancies": 1}]
    assert employer_data_db(data) == [{'company_id': "36227",
                                       'company_name': "000 МАГАЗИН МАГАЗИНОВ - Эксперт по торговой недвижимости",
                                       'company_url': "https://hh.ru/employer/36227",
                                       'vacancies_url': "https://api.hh.ru/vacancies?employer_id=36227",
                                       'amount_of_vacancies': 1
                                       }]


def test_vacancy_data_db():
    data = [
        {"id": "80099865", "premium": False, "name": "Диспетчер чатов, удаленно", "department": None, "has_test": False,
         "response_letter_required": False,
         "area": {"id": "113", "name": "Россия", "url": "https://api.hh.ru/areas/113"},
         "salary": {"from": 26000, "to": 40000, "currency": "RUR", "gross": False},
         "type": {"id": "open", "name": "Открытая"}, "address": None, "response_url": None, "sort_point_distance": None,
         "published_at": "2023-05-04T13:07:18+0300", "created_at": "2023-05-04T13:07:18+0300", "archived": False,
         "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=80099865",
         "insider_interview": None,
         "url": "https://api.hh.ru/vacancies/80099865?host=hh.ru", "adv_response_url": None,
         "alternate_url": "https://hh.ru/vacancy/80099865", "relations": [],
         "employer": {"id": "1740", "name": "Яндекс", "url": "https://api.hh.ru/employers/1740",
                      "alternate_url": "https://hh.ru/employer/1740",
                      "logo_urls": {"90": "https://hhcdn.ru/employer-logo/3790847.png",
                                    "240": "https://hhcdn.ru/employer-logo/3790848.png",
                                    "original": "https://hhcdn.ru/employer-logo-original/837491.png"},
                      "vacancies_url": "https://api.hh.ru/vacancies?employer_id=1740", "trusted": True},
         "snippet": {
             "requirement": "Опыт работы не требуется. Обязательно наличие ПК или ноутбука. Будет плюсом опыт работы на вакансиях:",
             "responsibility": None},
         "contacts": None, "schedule": None, "working_days": [],
         "working_time_intervals": [],
         "working_time_modes": [{"id": "start_after_sixteen", "name": "Можно начинать работать после 16:00"}],
         "accept_temporary": False, "professional_roles": [{"id": "40", "name": "Другое"}],
         "accept_incomplete_resumes": True, "experience": {"id": "noExperience", "name": "Нет опыта"},
         "employment": {"id": "full", "name": "Полная занятость"}}]

    assert vacancy_data_db(data) == [{'vacancy_id': "80099865",
                                      'vacancy_name': "Диспетчер чатов, удаленно",
                                      'vacancy_url': "https://hh.ru/vacancy/80099865",
                                      'salary_from': 26000,
                                      'salary_to': 40000,
                                      'currency': "RUR",
                                      'requirements': "Опыт работы не требуется. Обязательно наличие ПК или ноутбука. Будет плюсом опыт работы на вакансиях:",
                                      'responsibilities': None,
                                      'has_test': False,
                                      'employment': "Полная занятость",
                                      'company_id': "1740",
                                      'company_name': "Яндекс",
                                      'city': "Россия",
                                      'address': None
                                      }]
