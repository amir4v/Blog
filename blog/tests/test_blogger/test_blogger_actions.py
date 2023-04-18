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
class TestBloggerActions:
    def test_saved_posts_response_status_200(self, api_client, user, profile, post):
        profile.posts_saved.add(post)
        assert profile.posts_saved.filter(pk=post.pk).exists() == True
        
        saved_posts_path = reverse('blog:api-v1:blogger-saved-posts')
        api_client.force_login(user)
        response = api_client.get(saved_posts_path)
        assert response.status_code == 200
    
    def test_categories_response_status_200(self, api_client, user, category):
        categories_path = reverse('blog:api-v1:blogger-categories')
        api_client.force_login(user)
        response = api_client.get(categories_path)
        assert response.status_code == 200
    
    def test_category_posts_response_status_200(self, api_client, user, category, post):
        category.posts.add(post)
        assert category.posts.filter(pk=post.pk).exists() == True
        
        category_posts_path = reverse('blog:api-v1:blogger-category-posts',
                                      args=[category.pk])
        api_client.force_login(user)
        response = api_client.get(category_posts_path)
        assert response.status_code == 200
    
    def test_posts_response_status_200(self, api_client, user, post):
        posts_path = reverse('blog:api-v1:blogger-posts')
        api_client.force_login(user)
        response = api_client.get(posts_path)
        assert response.status_code == 200
    
    def test_liked_posts_response_status_200(self, api_client, user, profile, post):
        profile.posts_liked.add(post)
        assert profile.posts_liked.filter(pk=post.pk).exists() == True
        
        liked_posts_path = reverse('blog:api-v1:blogger-liked-posts')
        api_client.force_login(user)
        response = api_client.get(liked_posts_path)
        assert response.status_code == 200
    
    def test_comments_response_status_200(self, api_client, user, comment):
        comments_path = reverse('blog:api-v1:blogger-comments')
        api_client.force_login(user)
        response = api_client.get(comments_path)
        assert response.status_code == 200
    
    def test_liked_comments_response_status_200(self, api_client, user, profile, comment):
        profile.comments_liked.add(comment)
        assert profile.comments_liked.filter(pk=comment.pk).exists() == True
        
        liked_comments_path = reverse('blog:api-v1:blogger-liked-comments')
        api_client.force_login(user)
        response = api_client.get(liked_comments_path)
        assert response.status_code == 200
