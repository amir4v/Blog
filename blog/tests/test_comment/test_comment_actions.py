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
class TestCommentActions:
    def test_who_liked_response_status_200(self, api_client, user, profile, comment, post):
        profile.comments_liked.add(comment)
        assert profile.comments_liked.filter(pk=comment.pk).exists() == True
        
        who_liked_path = reverse('blog:api-v1:comment-who-liked',
                                 args=[comment.pk])
        api_client.force_login(user)
        response = api_client.get(who_liked_path)
        assert response.status_code == 200
    
    def test_like_response_status_200(self, api_client, user, comment):
        like_path = reverse('blog:api-v1:comment-like', args=[comment.pk])
        api_client.force_login(user)
        response = api_client.get(like_path)
        assert response.status_code == 200
    
    def test_unlike_response_status_200(self, api_client, user, profile, comment, post):
        profile.comments_liked.add(comment)
        assert profile.comments_liked.filter(pk=comment.pk).exists() == True
        
        like_path = reverse('blog:api-v1:comment-unlike', args=[comment.pk])
        api_client.force_login(user)
        response = api_client.get(like_path)
        assert response.status_code == 200
