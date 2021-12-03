from django.contrib.auth.hashers import check_password
from django.urls import reverse

from TriEvent_app.models import User, Athlete
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
def test_athlete_details_view(web_client, athlete):
    result = web_client.get(reverse('my-profile', args=[athlete.id]))
    assert result.context['first_name'] == athlete.first_name
    assert result.context['last_name'] == athlete.last_name
    assert result.context['proficiency'] == athlete.proficiency
    assert result.context['age_group'] == athlete.age_group
    assert result.context['created'] == athlete.created
    assert result.context['updated'] == athlete.updated
    assert result.context['last_login'] == athlete.last_login




