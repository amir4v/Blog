from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from blog.models import Category
from blog.api.v1.serializers import (
    PostModelSerializer,
    CategoryModelSerializer,
    CommentModelSerializer,
)

User = get_user_model()


class BloggerViewSet(ViewSet):
    """
    Blogger View Set
    ----------------
    A user can perform these actions:
        saved_posts
        categories
        category_posts
        posts
        liked_posts
        comments
        liked_comments
    """
    
    @action(detail=False, url_path='saved-posts')
    def saved_posts(self, request):
        """Get current user's saved posts."""
        
        profile = request.user.profile
        posts = profile.posts_saved.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False)
    def categories(self, request):
        """Get current user's categories."""
        
        profile = request.user.profile
        categories = profile.categories.all()
        serializer = CategoryModelSerializer(instance=categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='category-posts')
    def category_posts(self, request, pk):
        """Get current user's category's posts."""
        
        profile = request.user.profile
        category = get_object_or_404(Category, profile=profile, pk=pk)
        posts = category.posts.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False)
    def posts(self, request):
        """Get current user's posts."""
        
        profile = request.user.profile
        posts = profile.posts.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, url_path='liked-posts')
    def liked_posts(self, request):
        """Get current user's liked posts."""
        
        profile = request.user.profile
        posts = profile.posts_liked.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, url_path='comments')
    def comments(self, request):
        """Get current user's comments."""
        
        profile = request.user.profile
        comments = profile.comments.all()
        serializer = CommentModelSerializer(instance=comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, url_path='liked-comments')
    def liked_comments(self, request):
        """Get current user's liked comments."""
        
        profile = request.user.profile
        comments = profile.comments_liked.all()
        serializer = CommentModelSerializer(instance=comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
