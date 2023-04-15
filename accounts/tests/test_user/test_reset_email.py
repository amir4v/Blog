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
class TestResetEmail:
    def test_reset_email_send_link_response_status_200(self, api_client, user):
        reset_email_path = reverse('accounts:api-v1:user-reset-email')
        data = {
            'new_email': 'test-mail@example.com',
            'confirm_new_email': 'test-mail@example.com'
        }
        api_client.force_login(user)
        response = api_client.post(reset_email_path, data)
        assert response.status_code == 200
        
        user.email = data.get('new_email')
        token = get_activation_token(user)
        return token
    
    def test_reset_email_verify_response_status_200(self, api_client, user):
        token = self.test_reset_email_send_link_response_status_200(api_client, user)
        reset_email_verify_path = reverse('accounts:api-v1:user-reset-email-verify',
                                          args=[token])
        api_client.force_login(user)
        response = api_client.get(reset_email_verify_path)
        assert response.status_code == 200
