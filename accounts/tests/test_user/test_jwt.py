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
class TestJWT:
    def test_jwt_login_response_status_200_and_get_access_and_refresh_tokens(self, api_client, user, password):
        jwt_token_login_path = reverse('accounts:api-v1:token_obtain_pair')
        data = {'email': user.email, 'password': password}
        
        response = api_client.post(jwt_token_login_path, data)
        
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
        
        refresh = response.data.get('refresh')
        return refresh
    
    def test_jwt_token_refresh_response_status_200_and_get_access_token(self, api_client, user, password):
        refresh = self.test_jwt_login_response_status_200_and_get_access_and_refresh_tokens(api_client, user, password)
        
        jwt_token_login_path = reverse('accounts:api-v1:token_refresh')
        data = {'refresh': refresh}
        
        response = api_client.post(jwt_token_login_path, data)
        
        assert response.status_code == 200
        assert 'access' in response.data
