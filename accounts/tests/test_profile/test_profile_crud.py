from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
import pytest

from accounts.api.v1.views.profile import ProfileModelViewSet

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


@pytest.fixture
def password():
    return 'a/@12345678'


@pytest.fixture
def user(password):
    return User.objects.create_superuser(email='test@example.com',
                                         password=password, is_active=True)


@pytest.mark.django_db
class TestProfileCRUD:
    def test_retrieve_profile_response_status_200(self, api_client, user):
        retrieve_path = reverse('accounts:api-v1:profile-detail',
                                args=[user.pk])
        api_client.force_login(user)
        response = api_client.get(retrieve_path)
        assert response.status_code == 200
    
    def test_list_of_profiles_response_status_200(self, api_client, user):
        list_path = reverse('accounts:api-v1:profile-list')
        api_client.force_login(user)
        response = api_client.get(list_path)
        assert response.status_code == 200
    
    # def test_create_profile_response_status_201(self, api_client, user):
    #     pass
    
    def test_update_profile_response_status_200(self, api_request_factory, user):
        update_path = reverse('accounts:api-v1:profile-detail', args=[user.pk])
        
        view = ProfileModelViewSet.as_view({'put': 'update'})
        
        data = {
            'name': 'test-name',
            'profile_avatar': open(settings.BASE_DIR / 'accounts/tests/test_profile/image.png', 'rb')
        }
        
        request = api_request_factory.put(update_path, data=data)
        
        force_authenticate(request, user=user)
        
        response = view(request, pk=user.pk)
        
        assert response.status_code == 200
    
    def test_partial_update_profile_response_status_200(self, api_request_factory, user):
        update_path = reverse('accounts:api-v1:profile-detail', args=[user.pk])
        
        view = ProfileModelViewSet.as_view({'patch': 'partial_update'})
        
        data_1 = {
            'name': 'test-name-1',
        }
        data_2 = {
            'profile_avatar': open(settings.BASE_DIR / 'accounts/tests/test_profile/image.png', 'rb')
        }
        data_3 = {
            'name': 'test-name-3',
            'profile_avatar': open(settings.BASE_DIR / 'accounts/tests/test_profile/image.png', 'rb')
        }
        
        request = api_request_factory.patch(update_path, data=data_1)
        force_authenticate(request, user=user)
        response = view(request, pk=user.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_2)
        force_authenticate(request, user=user)
        response = view(request, pk=user.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_3)
        force_authenticate(request, user=user)
        response = view(request, pk=user.pk)
        assert response.status_code == 200
    
    def test_delete_profile_response_status_200(self, api_client, user):
        delete_path = reverse('accounts:api-v1:profile-detail', args=[user.pk])
        api_client.force_login(user)
        response = api_client.get(delete_path)
        assert response.status_code == 200
