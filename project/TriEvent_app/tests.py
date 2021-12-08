from django.contrib.auth.hashers import check_password
from django.urls import reverse

from TriEvent_app.models import User, Athlete, Race
import pytest

# models test


@pytest.mark.django_db
def test_add_user(web_client):
    assert User.objects.count() == 0
    username = "Szybki Bill"
    email = "bill@gmail.com"
    password = "hasłomasło"
    first_name = 'Bill',
    last_name = "Szybki",
    proficiency = "amateur",
    age_group = "60-64",
    post_data = {
        'username': username,
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'proficiency': proficiency,
        'age_group': age_group,
    }

    response = web_client.post(reverse('registration'), post_data)

    assert User.objects.count() == 1
    user = User.objects.first()
    assert user.username == username
    assert user.email == email
    assert check_password(encoded=user.password, password=password)


@pytest.mark.django_db
def test_add_race(web_client):
    name = 'Garmin Iron Triathlon Skierniewice 2022'
    organiser = 'Garmin'
    distance = '5'
    city = 'Skierniewice'
    voivodeship = '5'
    description = 'Garmin Iron Triathlon Skierniewice 2022 zostanie rozegrany na ' \
                  'trzech dystansach: 1/2 IM, 1/4 IM oraz 1/8 IM! Na każdym z dystansów' \
                  ' będzie można wystartować w trzyosobowej sztafecie triathlonowej.'
    race_url = 'https://irontriathlon.pl/skierniewice-menu/'
    date = '2022-07-03'
    post_data = {
        'name': name,
        'organiser': organiser,
        'distance': distance,
        'city': city,
        'voivodeship': voivodeship,
        'description': description,
        'race_url': race_url,
        'date': date
    }

    response = web_client.post(reverse('races-list')),

    race = Race.objects.first()
    assert race.name == name
    assert race.organiser == organiser
    assert race.distance == distance
    assert race.city == city
    assert race.voivodeship == voivodeship
    assert race.description == description
    assert race.race_url == race_url
    assert race.date == date






