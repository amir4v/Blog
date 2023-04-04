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
class TestUserCRUD:
    def test_retrieve_response_status_200(self, api_client, user):
        retrieve_path = reverse('accounts:api-v1:user-detail', args=[user.pk])
        api_client.force_login(user)
        response = api_client.get(retrieve_path)
        assert response.status_code == 200
