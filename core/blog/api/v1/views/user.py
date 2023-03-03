from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action

from accounts.models import *
from blog.models import *
from blog.api.v1.serializers import *


User = get_user_model()


class BloggerViewSet(ViewSet):
    @action(detail=False, methods=['get'], url_path='saved-posts')
    def saved_posts(self, request):
        profile = request.user.profile
        posts = profile.posts_saved.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='categories')
    def categories(self, request):
        profile = request.user.profile
        categories = profile.categories.all()
        serializer = CategoryModelSerializer(instance=categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='posts')
    def posts(self, request):
        profile = request.user.profile
        posts = profile.posts.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='liked-posts')
    def liked_posts(self, request):
        profile = request.user.profile
        posts = profile.posts_liked.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='comments')
    def comments(self, request):
        profile = request.user.profile
        comments = profile.comments.all()
        serializer = CommentModelSerializer(instance=comments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='liked-comments')
    def liked_comments(self, request):
        profile = request.user.profile
        comments = profile.comments_liked.all()
        serializer = CommentModelSerializer(instance=comments, many=True)
        return Response(serializer.data)
