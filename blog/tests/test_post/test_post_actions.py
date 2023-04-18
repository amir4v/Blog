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
    return Post.objects.create(title='test-post', content='test-content',
                               profile=profile, category=category)


@pytest.fixture
def comment(profile, post):
    return Comment.objects.create(comment='test-comment',
                                  profile=profile,
                                  post=post)


@pytest.mark.django_db
class TestPostActions:
    def test_who_liked_response_status_200(self, api_client, user, profile, post):
        profile.posts_liked.add(post)
        assert profile.posts_liked.filter(pk=post.pk).exists() == True
        
        who_liked_path = reverse('blog:api-v1:post-who-liked', args=[post.pk])
        api_client.force_login(user)
        response = api_client.get(who_liked_path)
        assert response.status_code == 200
    
    def test_comments_response_status_200(self, api_client, user, post, comment):
        post.comments.add(comment)
        assert post.comments.filter(pk=comment.pk).exists() == True
        
        comments_path = reverse('blog:api-v1:post-comments', args=[post.pk])
        api_client.force_login(user)
        response = api_client.get(comments_path)
        assert response.status_code == 200
    
    def test_like_response_status_200(self, api_client, user, post):
        like_path = reverse('blog:api-v1:post-like', args=[post.pk])
        api_client.force_login(user)
        response = api_client.get(like_path)
        assert response.status_code == 200
    
    def test_unlike_response_status_200(self, api_client, user, profile, post):
        profile.posts_liked.add(post)
        assert profile.posts_liked.filter(pk=post.pk).exists() == True
        
        like_path = reverse('blog:api-v1:post-unlike', args=[post.pk])
        api_client.force_login(user)
        response = api_client.get(like_path)
        assert response.status_code == 200
    
    def test_save_response_status_200(self, api_client, user, post):
        save_path = reverse('blog:api-v1:post-save', args=[post.pk])
        api_client.force_login(user)
        response = api_client.get(save_path)
        assert response.status_code == 200
    
    def test_unsave_response_status_200(self, api_client, user, profile, post):
        profile.posts_saved.add(post)
        assert profile.posts_saved.filter(pk=post.pk).exists() == True
        
        unsave_path = reverse('blog:api-v1:post-unsave', args=[post.pk])
        api_client.force_login(user)
        response = api_client.get(unsave_path)
        assert response.status_code == 200
