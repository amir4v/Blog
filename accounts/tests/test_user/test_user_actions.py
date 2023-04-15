from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def password():
    return 'a/@12345678'


@pytest.fixture
def user(password) -> User:
    return User.objects.create_superuser(email='test@example.com', password=password, is_active=True)


@pytest.mark.django_db
class TestUserActions:
    def test_pre_register_response_status_200(self, api_client, user):
        pre_register_path = reverse('accounts:api-v1:user-pre-register')
        
        """Sending an existing email to fail."""
        fail_data = {
            'email': user.email
        }
        response = api_client.post(pre_register_path, data=fail_data)
        assert response.status_code == 400
        
        data = {
            'email': 'test-pre-register@example.com'
        }
        response = api_client.post(pre_register_path, data=data)
        assert response.status_code == 200
    
    def test_register_response_status_200(self, api_client, user):
        user.password = ''
        # user.is_active = False
        user.is_verified = False
        user.is_staff = False
        user.is_superuser = False
        user.save()
        
        register_path = reverse('accounts:api-v1:user-register')
        data = {
            'new_password': 'asdf1234!@#$',
            'confirm_new_password': 'asdf1234!@#$',
        }
        api_client.force_login(user)
        response = api_client.post(register_path, data=data)
        assert response.status_code == 200
    
    def test_me_response_status_200(self, api_client, user):
        me_path = reverse('accounts:api-v1:user-me')
        api_client.force_login(user)
        response = api_client.get(me_path)
        assert response.status_code == 200
    
    def test_profile_response_status_200(self, api_client, user):
        profile_path = reverse('accounts:api-v1:user-profile')
        api_client.force_login(user)
        response = api_client.get(profile_path)
        assert response.status_code == 200
    
    def test_reset_password_response_status_200(self, api_client, user, password):
        reset_password_path = reverse('accounts:api-v1:user-reset-password')
        data = {
            'old_password': password,
            'new_password': '12345678as!@AS',
            'confirm_new_password': '12345678as!@AS',
        }
        api_client.force_login(user)
        response = api_client.post(reset_password_path, data)
        assert response.status_code == 200
    
    def test_reset_username_response_status_200(self, api_client, user):
        reset_username_path = reverse('accounts:api-v1:user-reset-username')
        data = {
            'new_username': 'newusername123'
        }
        api_client.force_login(user)
        response = api_client.post(reset_username_path, data)
        assert response.status_code == 200
    
    def test_login_pages_response_status_200(self, api_client, user, password):
        straight_login_path = '/login/'
        login_path = reverse('accounts:api-v1:user-list') + straight_login_path[1:]
        
        data = {
            'email': user.email,
            'password': password
        }
        data_using_username = {
            'email': user.username,
            'password': password
        }
        
        response = api_client.post(straight_login_path, data=data)
        assert response.status_code == 200
        """Using username"""
        response = api_client.post(straight_login_path, data=data_using_username)
        assert response.status_code == 200
        
        response = api_client.post(login_path, data=data)
        assert response.status_code == 200
        """Using username"""
        response = api_client.post(login_path, data=data_using_username)
        assert response.status_code == 200
    
    def test_logout_response_204(self, api_client, user):
        logout_path = reverse('accounts:api-v1:user-logout')
        api_client.force_login(user)
        response = api_client.get(logout_path)
        assert response.status_code == 204
