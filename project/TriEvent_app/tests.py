from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.urls import reverse

from TriEvent_app.conftest import web_client, new_race
from TriEvent_app.models import User, Race
import pytest


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
def test_login(web_client):
    assert User.objects.count() == 0
    User.objects.create_user(username="User", password="Password")
    assert User.objects.count() == 1
    post_data = {
        'username': 'User',
        'password': 'Password'
    }
    response = web_client.post(reverse('login'), post_data)
    assert response.status_code == 302
    assert authenticate(username='User', password='Password')


@pytest.mark.django_db
def test_logout(web_client, new_user):
    assert new_user.is_authenticated
    response = web_client.get(reverse('logout'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_races_list_view(web_client, list_of_races):
    response = web_client.get('/races')
    assert response.status_code == 301
    races = response.context['races_list']
    assert races == list_of_races









