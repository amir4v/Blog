"""
user/
    pre-register/
    register/
    me/
    profile/
    reset-password/
    reset-username/
    # /login/
    # login/
    logout/
"""

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def password():
    return 'a/@12345678'


@pytest.fixture
def user(password):
    return User.objects.create_superuser(email='test@example.com', password=password, is_active=True)


@pytest.mark.django_db
class TestUserActions:
    pass
