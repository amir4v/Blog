from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
import pytest

from blog.models import Category, Post
from blog.api.v1.views.post import PostModelViewSet

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
                                         password=password,
                                         is_active=True)


@pytest.fixture
def profile(user):
    return user.profile


@pytest.fixture
def test_profile(password):
    return User.objects.create_superuser(email='test-profile@example.com',
                                         password=password,
                                         is_active=True).profile


@pytest.fixture
def category(profile):
    return Category.objects.create(name='category', profile=profile)


@pytest.fixture
def test_category(test_profile):
    return Category.objects.create(name='test-category', profile=test_profile)


@pytest.fixture
def post(profile, category):
    return Post.objects.create(title='test-post', content='test-content',
                               profile=profile, category=category)


@pytest.mark.django_db
class TestPostCRUD:
    def test_retrieve_post_response_status_200(self, api_client, user, post):
        retrieve_path = reverse('blog:api-v1:post-detail',
                                args=[post.pk])
        api_client.force_login(user)
        response = api_client.get(retrieve_path)
        assert response.status_code == 200
    
    def test_list_of_posts_response_status_200(self, api_client, user, post):
        list_path = reverse('blog:api-v1:post-list')
        api_client.force_login(user)
        response = api_client.get(list_path)
        assert response.status_code == 200
    
    def test_create_post_response_status_201(self, api_client, user, profile, category):
        create_path = reverse('blog:api-v1:post-list')
        api_client.force_login(user)
        data = {
            'title': 'test-create-post',
            'content': 'test-create-post-content',
            'profile': profile.pk,
            'category': category.pk,
        }
        response = api_client.post(create_path, data=data)
        assert response.status_code == 201
    
    def test_update_post_response_status_200(self, api_request_factory, user, post, test_profile, test_category):
        update_path = reverse('blog:api-v1:post-detail', args=[post.pk])
        
        view = PostModelViewSet.as_view({'put': 'update'})
        
        data = {
            'title': 'test-update-post',
            'content': 'test-update-post-content',
            'profile': test_profile.pk,
            'category': test_category.pk,
        }
        
        request = api_request_factory.put(update_path, data=data)
        
        force_authenticate(request, user=user)
        
        response = view(request, pk=user.pk)
        
        assert response.status_code == 200
    
    def test_partial_update_post_response_status_200(self, api_request_factory, user, post, test_profile, test_category):
        update_path = reverse('blog:api-v1:post-detail', args=[post.pk])
        
        view = PostModelViewSet.as_view({'patch': 'partial_update'})
        
        data_1 = {
            'title': 'test-update-1-post',
        }
        data_2 = {
            'content': 'test-update-post-content-2',
        }
        data_3 = {
            'category': test_category.pk,
        }
        data_4 = {
            'profile': test_profile.pk,
        }
        data_5 = {
            'title': 'test-update-post-5',
            'content': 'test-update-post-content-5',
            'profile': test_profile.pk,
            'category': test_category.pk,
        }
        
        request = api_request_factory.patch(update_path, data=data_1)
        force_authenticate(request, user=user)
        response = view(request, pk=post.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_2)
        force_authenticate(request, user=user)
        response = view(request, pk=post.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_3)
        force_authenticate(request, user=user)
        response = view(request, pk=post.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_4)
        force_authenticate(request, user=user)
        response = view(request, pk=post.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_5)
        """In this request we change the user, because it(the post owner) changed in the previous request."""
        force_authenticate(request, user=test_profile.user)
        response = view(request, pk=post.pk)
        assert response.status_code == 200
    
    def test_delete_post_response_status_200(self, api_client, user, post):
        delete_path = reverse('blog:api-v1:post-detail', args=[post.pk])
        api_client.force_login(user)
        response = api_client.get(delete_path)
        assert response.status_code == 200
