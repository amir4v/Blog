from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
import pytest
import requests

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
def profile_a(password):
    return User.objects.create_superuser(email='test-a@example.com', password=password, is_active=True).profile


@pytest.fixture
def profile_b(password):
    return User.objects.create_superuser(email='test-b@example.com', password=password, is_active=True).profile


@pytest.mark.django_db
class TestFollowingSystem:
    def test_follow_response_status_200(self, profile_a, profile_b):
        profile_a.followings.add(profile_b)
        assert profile_a.followings.filter(pk=profile_b).exists() == True
    
    def test_unfollow_response_status_200(self, profile_a, profile_b):
        profile_a.followings.add(profile_b)
        assert profile_a.followings.filter(pk=profile_b).exists() == True
        
        profile_a.followings.remove(profile_b)
        assert profile_a.followings.filter(pk=profile_b).exists() == False
    
    def test_followers_response_status_200(self, api_client, profile_a, profile_b):
        profile_a.followings.add(profile_b)
        assert profile_a.followings.filter(pk=profile_b).exists() == True
        
        followers_path = reverse('blog:api-v1:blogger-followers')
        api_client.force_login(profile_b.user)
        response = api_client.get(followers_path)
        assert response.status_code == 200
    
    def test_followings_response_status_200(self, api_client, profile_a, profile_b):
        profile_a.followings.add(profile_b)
        assert profile_a.followings.filter(pk=profile_b).exists() == True
        
        followings_path = reverse('blog:api-v1:blogger-followings')
        api_client.force_login(profile_a.user)
        response = api_client.get(followings_path)
        assert response.status_code == 200
    
    def test_do_i_follow_you_response_status_200(self, api_client, profile_a, profile_b):
        profile_a.followings.add(profile_b)
        assert profile_a.followings.filter(pk=profile_b).exists() == True
        
        follow_path = reverse('blog:api-v1:blogger-do-i-follow-you', args=[profile_b.pk])
        api_client.force_login(profile_a.user)
        response = api_client.get(follow_path)
        assert response.status_code == 200
    
    def test_do_you_follow_me_response_status_200(self, api_client, profile_a, profile_b):
        profile_a.followings.add(profile_b)
        assert profile_a.followings.filter(pk=profile_b).exists() == True
        
        follow_path = reverse('blog:api-v1:blogger-do-you-follow-me', args=[profile_a.pk])
        api_client.force_login(profile_b.user)
        response = api_client.get(follow_path)
        assert response.status_code == 200
