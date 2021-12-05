import pytest
from django.test import Client

from TriEvent_app.models import Race


@pytest.fixture
def web_client():
    c = Client()
    return c


@pytest.fixture
def new_race():
    r = Race()
    r.name = 'Garmin Iron Triathlon Skierniewice 2022'
    r.organiser = 'Garmin'
    r.distance = '5'
    r.city = 'Skierniewice'
    r.voivodeship = '5'
    r.description = 'Garmin Iron Triathlon Skierniewice 2022 zostanie rozegrany na trzech dystansach: 1/2 IM, 1/4 IM oraz 1/8 IM! Na każdym z dystansów będzie można wystartować w trzyosobowej sztafecie triathlonowej.'
    r.race_url = 'https://irontriathlon.pl/skierniewice-menu/'
    r.date = '2022-07-03'
    r.save()
    return r


