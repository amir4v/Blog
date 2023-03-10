from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework import status

from accounts.models import Profile
from blog.models import *
from blog.api.v1.serializers import *
from accounts.api.v1.serializers import *


User = get_user_model()


class PagesViewSet(ViewSet):
    """
    home
    top
    latest
    post search
    profile search
    """
    
    @action(detail=False, methods=['get'])
    def home(self, request):
        profile = request.user.profile
        posts = Post.objects.filter(
            profile__in=profile.followings.values('user_id')
        ).order_by('-created_at')
        data = PostModelSerializer(instance=posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """
        created_at
        seen
        likes
        """
        profile = request.user.profile
        posts = Post.objects.order_by('-created_at').order_by('-seen').annotate(likes=Count('who_liked')).order_by('-likes')
        data = PostModelSerializer(instance=posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        posts = Post.objects.order_by('-created_at')
        data = PostModelSerializer(instance=posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='search-post')
    def search_post(self, request, pk):
        posts = Post.objects.filter(title__icontains=pk).order_by('-created_at')
        data = PostModelSerializer(instance=posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='search-profile')
    def search_profile(self, request, pk):
        profiles = User.objects.filter(username__icontains=pk).values('profile').order_by('?')
        data = ProfileModelSerializer(instance=profiles, many=True).data
        return Response(data, status=status.HTTP_200_OK)
