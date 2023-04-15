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
class TestForgotPassword:
    def test_forgot_password_for_authenticated_user_response_status_200(self, api_client, user):
        forgot_password_path = reverse('accounts:api-v1:user-forgot-password')
        api_client.force_login(user)
        response = api_client.get(forgot_password_path)
        assert response.status_code == 200
    
    def test_forgot_password_confirm_for_unauthenticated_user_response_status_200(self, api_client, user):
        forgot_password_confirm_path = reverse('accounts:api-v1:user-forgot-password-confirm')
        data = {'email': user.email}
        response = api_client.post(forgot_password_confirm_path, data)
        assert response.status_code == 200
        
        token = get_activation_token(user)
        return token
    
    def test_forgot_password_verify_response_status_200(self, api_client, user):
        token = self.test_forgot_password_confirm_for_unauthenticated_user_response_status_200(api_client, user)
        forgot_password_verify_path = reverse('accounts:api-v1:user-forgot-password-verify',
                                              args=[token])
        response = api_client.get(forgot_password_verify_path)
        assert response.status_code == 200
