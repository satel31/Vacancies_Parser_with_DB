import pytest
from src.requests_classes import EmployerRequest, VacancyRequest


@pytest.fixture
def employer():
    return EmployerRequest('develop')


def test_employer_request_init(employer):
    """Test of initialization of the class HHRequest without new per_page"""
    assert employer.key_word == 'develop'


def test_employer_request_get_id(employer):
    """Test of request_data method with responce status 200"""
    data = employer.get_id(employer.request_data())
    assert data == ['4488910', '3304233', '46926', '5724503', '2081468', '4823', '5075716', '2367681', '5451',
                    '2788545',
                    '805692', '5920997', '4661352', '5499295', '5585118']


def test_vacancy_request_init():
    data = ['4488910', '3304233', '46926', '5724503', '2081468', '4823', '5075716', '2367681', '5451', '2788545',
            '805692', '5920997', '4661352', '5499295', '5585118']
    vr = VacancyRequest(data)
    assert vr.employer_ids == data
