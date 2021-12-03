import pytest
from django.test import Client

from TriEvent_app.models import User, Athlete, Race, Results, Review


@pytest.fixture
def web_client():
    c = Client()
    return c

@pytest.fixture
def athlete():
    a = Athlete()
    a.first_name = 'Anna'
    a.last_name = 'Brygas'
    a.proficiency = 'amateur'
    a.age_group = '20-24'
    a.created = '2021-11-29 22:21:53'
    a.updated = '2021-11-29 22:21:53'
    a.last_login = '2021-11-29 22:21:53'

