import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def client_auth():
    u = User.objects.create(username='test')
    u.set_password('123')
    u.save()
    client = APIClient()
    client.login(username='test', password='123')

    yield client
    client.logout()
