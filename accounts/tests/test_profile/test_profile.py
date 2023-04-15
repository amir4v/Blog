from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(password):
    return User.objects.create_superuser(email='test@example.com', password=password, is_active=True)


@pytest.mark.django_db
class TestProfile:
    def test_retrieve_a_user_response_status_200(self, api_client, user):
        retrieve_path = reverse('accounts:api-v1:user-detail', args=[user.pk])
        api_client.force_login(user)
        response = api_client.get(retrieve_path)
        assert response.status_code == 200
    
    def test_list_of_users_response_status_200(self, api_client, user):
        list_path = reverse('accounts:api-v1:user-list')
        api_client.force_login(user)
        response = api_client.get(list_path)
        assert response.status_code == 200
    
    def test_create_a_user_response_status_201(self, api_client, user):
        create_path = reverse('accounts:api-v1:user-list')
        api_client.force_login(user)
        data = {
            'email': 'create-user-test@example.com',
            'password': 'asdf1234!@#$',
            'confirm_password': 'asdf1234!@#$',
        }
        response = api_client.post(create_path, data=data)
        assert response.status_code == 201
    
    def test_update_a_user_response_status_405(self, api_client, user):
        update_path = reverse('accounts:api-v1:user-detail', args=[user.pk])
        api_client.force_login(user)
        data = {
            'email': 'update-user-test@example.com',
            'password': 'asdf1234!@#$',
            'confirm_password': 'asdf1234!@#$',
        }
        response = api_client.post(update_path, data=data)
        assert response.status_code == 405
    
    # def test_partial_update_a_user_response_status_405
    
    def test_delete_a_user_response_status_200(self, api_client, user):
        delete_path = reverse('accounts:api-v1:user-detail', args=[user.pk])
        api_client.force_login(user)
        response = api_client.get(delete_path)
        assert response.status_code == 200
