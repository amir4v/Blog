from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from blog.models import Post
from blog.api.v1.serializers import PostModelSerializer
from accounts.api.v1.serializers import ProfileModelSerializer

User = get_user_model()


class PagesViewSet(ViewSet):
    """
    Page View Set
    -------------
    A user can perform these actions:
        home
        top
        latest
        search_post
        search_profile
    """
    
    @method_decorator(cache_page(15 * 60))
    @action(detail=False)
    def home(self, request):
        """
        Get posts from current user's followings' posts
        ordered by created_at in descending.
        """
        
        profile = request.user.profile
        posts = Post.objects.filter(
            profile__in=profile.followings.values('user_id')
        ).order_by('-created_at')
        data = PostModelSerializer(instance=posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @method_decorator(cache_page(15 * 60))
    @action(detail=False)
    def top(self, request):
        """
        Get latest posts ordered by seen in descending and
        likes in descending.
        """
        
        posts = Post.objects \
                        .order_by('-created_at') \
                        .order_by('-seen') \
                        .annotate(likes=Count('who_liked')) \
                        .order_by('-likes')
        data = PostModelSerializer(instance=posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @method_decorator(cache_page(15 * 60))
    @action(detail=False)
    def latest(self, request):
        """Get latest posts."""
        
        posts = Post.objects.order_by('-created_at')
        data = PostModelSerializer(instance=posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='search-post')
    def search_post(self, request, pk):
        """Search in posts with the given title ordered by created_at in descending."""
        
        posts = Post.objects.filter(title__icontains=pk) \
                            .order_by('-created_at')
        data = PostModelSerializer(instance=posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='search-profile')
    def search_profile(self, request, pk):
        """Search in profiles with the given username."""
        
        profiles = User.objects.filter(username__icontains=pk) \
                               .values('profile').order_by('?')
        data = ProfileModelSerializer(instance=profiles, many=True).data
        return Response(data, status=status.HTTP_200_OK)
