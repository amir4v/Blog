from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
import pytest

from blog.models import Category, Post
from blog.api.v1.views.category import CategoryModelViewSet

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
    return Category.objects.create(name='test-category', profile=profile)


@pytest.fixture
def post(profile, category):
    return Post.objects.create(title='test-post', content='test-content',
                               profile=profile, category=category)


@pytest.mark.django_db
class TestCategoryCRUD:
    """Test Category CRUD + posts action."""
    
    def test_retrieve_category_response_status_200(self, api_client, user, category):
        retrieve_path = reverse('blog:api-v1:category-detail',
                                args=[category.pk])
        api_client.force_login(user)
        response = api_client.get(retrieve_path)
        assert response.status_code == 200
    
    def test_list_of_categories_response_status_200(self, api_client, user, category):
        list_path = reverse('blog:api-v1:category-list')
        api_client.force_login(user)
        response = api_client.get(list_path)
        assert response.status_code == 200
    
    def test_create_category_response_status_201(self, api_client, user, profile):
        create_path = reverse('blog:api-v1:category-list')
        api_client.force_login(user)
        data = {
            'name': 'test-create-category',
            'profile': profile.pk
        }
        response = api_client.post(create_path, data=data)
        assert response.status_code == 201
    
    def test_update_category_response_status_200(self, api_request_factory, user, test_profile, category):
        update_path = reverse('blog:api-v1:category-detail',
                              args=[category.pk])
        
        view = CategoryModelViewSet.as_view({'put': 'update'})
        
        data = {
            'name': 'test-name-0',
            'profile': test_profile.pk
        }
        
        request = api_request_factory.put(update_path, data=data)
        
        force_authenticate(request, user=user)
        
        response = view(request, pk=user.pk)
        
        assert response.status_code == 200
    
    def test_partial_update_category_response_status_200(self, api_request_factory, user, test_profile, category):
        update_path = reverse('blog:api-v1:category-detail',
                              args=[category.pk])
        
        view = CategoryModelViewSet.as_view({'patch': 'partial_update'})
        
        data_1 = {
            'name': 'test-name-1',
        }
        data_2 = {
            'profile': test_profile.pk
        }
        data_3 = {
            'name': 'test-name-3',
            'profile': test_profile.pk
        }
        
        request = api_request_factory.patch(update_path, data=data_1)
        force_authenticate(request, user=user)
        response = view(request, pk=category.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_2)
        force_authenticate(request, user=user)
        response = view(request, pk=category.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_3)
        """In this request we change the user, because it(the category owner) changed in the previous request."""
        force_authenticate(request, user=test_profile.user)
        response = view(request, pk=category.pk)
        assert response.status_code == 200
    
    def test_delete_category_response_status_200(self, api_client, user, category):
        delete_path = reverse('blog:api-v1:category-detail',
                              args=[category.pk])
        api_client.force_login(user)
        response = api_client.get(delete_path)
        assert response.status_code == 200
    
    def test_category_posts_response_status_200(self, api_client, user, category, post):
        list_path = reverse('blog:api-v1:category-posts', args=[category.pk])
        api_client.force_login(user)
        response = api_client.get(list_path)
        assert response.status_code == 200
