from src.requests_classes import EmployerRequest

def employer_data_db(employer_data):
    employer_db = []
    for employer in employer_data:
        employer = {'company_id': employer['id'],
                    'company_name': employer['name'],
                    'company_url': employer['alternate_url'],
                    'vacancies_url': employer['vacancies_url'],
                    'amount_of_vacancies': employer['open_vacancies']
                    }
        employer_db.append(employer)
    return employer_db
