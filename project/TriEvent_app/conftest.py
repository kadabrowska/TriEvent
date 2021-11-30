import pytest
from django.test import Client

from TriEvent_app.models import User, Athlete, Race, Results, Review


@pytest.fixture
def web_client():
    c = Client()
    return c

