from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
import pytest

from blog.models import Category, Post, Comment

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
                                         password=password,
                                         is_active=True)


@pytest.fixture
def profile(user):
    return user.profile


@pytest.fixture
def category(profile):
    return Category.objects.create(name='category', profile=profile)


@pytest.fixture
def post(profile, category):
    return Post.objects.create(title='post', content='test-content',
                               profile=profile, category=category)


@pytest.fixture
def comment(profile, post):
    return Comment.objects.create(comment='test-comment',
                                  profile=profile, post=post)


@pytest.mark.django_db
class TestPages:
    def test_home_response_status_200(self, api_client, user):
        saved_posts_path = reverse('blog:api-v1:pages-home')
        api_client.force_login(user)
        response = api_client.get(saved_posts_path)
        assert response.status_code == 200
    
    def test_top_response_status_200(self, api_client, user):
        saved_posts_path = reverse('blog:api-v1:pages-top')
        api_client.force_login(user)
        response = api_client.get(saved_posts_path)
        assert response.status_code == 200
    
    def test_latest_response_status_200(self, api_client, user):
        saved_posts_path = reverse('blog:api-v1:pages-latest')
        api_client.force_login(user)
        response = api_client.get(saved_posts_path)
        assert response.status_code == 200
    
    def test_search_post_response_status_200(self, api_client, user, post):
        search_post_path = reverse('blog:api-v1:pages-search-post',
                                   args=[post.title])
        api_client.force_login(user)
        response = api_client.get(search_post_path)
        assert response.status_code == 200
    
    def test_search_profile_response_status_200(self, api_client, user, profile):
        search_profile_path = reverse('blog:api-v1:pages-search-profile',
                                      args=[profile.user.username])
        api_client.force_login(user)
        response = api_client.get(search_profile_path)
        assert response.status_code == 200
