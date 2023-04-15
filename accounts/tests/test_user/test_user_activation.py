from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
import pytest

from accounts.utils import get_activation_token

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def password():
    return 'a/@12345678'


@pytest.fixture
def user(password):
    return User.objects.create_superuser(email='test@example.com',
                                         password=password, is_active=True)


@pytest.mark.django_db
class TestUserActivation:
    def test_pre_register_response_status_200(self, api_client):
        pre_register_path = reverse('accounts:api-v1:user-pre-register')
        data = {'email': 'pre-register-test@example.com'}
        response = api_client.post(pre_register_path, data)
        assert response.status_code == 200
        
        user = User(email=data.get('email'))
        token = get_activation_token(user)
        return token
    
    def test_user_activation_response_status_200(self, api_client):
        token = self.test_pre_register_response_status_200(api_client)
        user_activation = reverse('accounts:api-v1:user-activation',
                                  args=[token])
        response = api_client.get(user_activation)
        assert response.status_code == 200
    
    """No need for this"""
    # def test_user_activation_confirm_response_status_200(self, api_client):
    #     user_activation_confirm = reverse('accounts:api-v1:user-activation-confirm')
    #     data = {'email': 'pre-register-test@example.com'}
    #     response = api_client.post(user_activation_confirm, data)
    #     assert response.status_code == 200
