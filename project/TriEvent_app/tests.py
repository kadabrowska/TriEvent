from django.urls import reverse

from TriEvent_app.models import User
import pytest

# models test


@pytest.mark.django_db
def test_user_details_view(web_client, new_user):
    result = web_client.get(reverse('user', args=[new_user.id]))
    assert result.status.code == 200
    assert result.context['username'] == new_user.username
    assert result.context['email'] == new_user.email
    assert result.context['password'] == new_user.password


@pytest.mark.django_db
def test_add_user(web_client):
    assert User.objects.count() == 0
    username = "Szybki Bill"
    email = "bill@gmail.com"
    password = "hasłomasło"
    post_data = {
        'username': username,
        'email': email,
        'password': password
    }

    response = web_client.post(reverse('add-user'), post_data)

    assert User.objects.count() == 1
    user = User.objects.first()
    assert user.username == username
    assert user.email == email
    assert user.password == password

