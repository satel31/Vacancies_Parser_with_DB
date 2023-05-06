import requests


def request_data() -> dict:
    """Get data from hh.ru"""

    params: dict = {
        "per_page": 20,
        "area": 113
    }
    response = requests.get('https://api.hh.ru/employers', params=params)

    if response.status_code == 200:
        employers = response.json()['items']
        return employers
    else:
        print("Error:", response.status_code)


data = request_data()
print(data)
print(len(data))
for d in data:
    print(d)
    print()
#new_data = pass_by_page(data)
#print(new_data)
#print(len(new_data))