from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
import pytest

from blog.models import Category, Post, Comment
from blog.api.v1.views.comment import CommentModelViewSet

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
def post(profile, category):
    return Post.objects.create(title='post', content='test-content',
                               profile=profile, category=category)


@pytest.fixture
def test_post(profile, category):
    return Post.objects.create(title='test-post', content='test-content',
                               profile=profile, category=category)


@pytest.fixture
def comment(profile, post):
    return Comment.objects.create(comment='test-comment',
                                  profile=profile, post=post)


@pytest.mark.django_db
class TestCommentCRUD:
    def test_retrieve_comment_response_status_200(self, api_client, user, comment):
        retrieve_path = reverse('blog:api-v1:comment-detail',
                                args=[comment.pk])
        api_client.force_login(user)
        response = api_client.get(retrieve_path)
        assert response.status_code == 200
    
    def test_list_of_comments_response_status_200(self, api_client, user, comment):
        list_path = reverse('blog:api-v1:comment-list')
        api_client.force_login(user)
        response = api_client.get(list_path)
        assert response.status_code == 200
    
    def test_create_comment_response_status_201(self, api_client, user, profile, post):
        create_path = reverse('blog:api-v1:comment-list')
        api_client.force_login(user)
        data = {
            'comment': 'test-create-comment',
            'post': post.pk,
            'profile': profile.pk,
        }
        response = api_client.post(create_path, data=data)
        assert response.status_code == 201
    
    def test_update_comment_response_status_200(self, api_request_factory, user, test_profile, comment, test_post):
        update_path = reverse('blog:api-v1:comment-detail', args=[comment.pk])
        
        view = CommentModelViewSet.as_view({'put': 'update'})
        
        data = {
            'comment': 'test-update-comment',
            'post': test_post.pk,
            'profile': test_profile.pk,
        }
        
        request = api_request_factory.put(update_path, data=data)
        
        force_authenticate(request, user=user)
        
        response = view(request, pk=user.pk)
        
        assert response.status_code == 200
    
    def test_partial_update_comment_response_status_200(self, api_request_factory, user, test_profile, comment, test_post):
        update_path = reverse('blog:api-v1:comment-detail', args=[comment.pk])
        
        view = CommentModelViewSet.as_view({'patch': 'partial_update'})
        
        data_1 = {
            'comment': 'test-update-comment-1',
        }
        data_2 = {
            'post': test_post.pk,
        }
        data_3 = {
            'profile': test_profile.pk,
        }
        data_4 = {
            'comment': 'test-update-comment-4',
            'post': test_post.pk,
            'profile': test_profile.pk,
        }
        
        request = api_request_factory.patch(update_path, data=data_1)
        force_authenticate(request, user=user)
        response = view(request, pk=comment.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_2)
        force_authenticate(request, user=user)
        response = view(request, pk=comment.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_3)
        force_authenticate(request, user=user)
        response = view(request, pk=comment.pk)
        assert response.status_code == 200
        
        request = api_request_factory.patch(update_path, data=data_4)
        """In this request we change the user, because it(the comment owner) changed in the previous request."""
        force_authenticate(request, user=test_profile.user)
        response = view(request, pk=comment.pk)
        assert response.status_code == 200
    
    def test_delete_comment_response_status_200(self, api_client, user, comment):
        delete_path = reverse('blog:api-v1:comment-detail', args=[comment.pk])
        api_client.force_login(user)
        response = api_client.get(delete_path)
        assert response.status_code == 200
