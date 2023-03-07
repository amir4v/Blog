from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework import status

from accounts.models import *
from blog.models import *
from blog.api.v1.serializers import *
from accounts.api.v1.serializers import *


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
    
    @action(detail=True, methods=['get'], url_path='category-posts')
    def category_posts(self, request, pk):
        profile = request.user.profile
        posts = profile.categories.get(pk=pk).posts.all()
        serializer = PostModelSerializer(instance=posts, many=True)
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
    
    @action(detail=True, methods=['get'])
    def follow(self, request, pk):
        profile = request.user.profile
        profile.followings.add(pk)
        return Response({'detail': 'Successfully followed.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def unfollow(self, request, pk):
        profile = request.user.profile
        profile.followings.remove(pk)
        return Response({'detail': 'Successfully un-followed.'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def followers(self, request):
        profile = request.user.profile
        fs = profile.followers.all()
        serializer = ProfileModelSerializer(instance=fs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def followings(self, request):
        profile = request.user.profile
        fs = profile.followings.all()
        serializer = ProfileModelSerializer(instance=fs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='do-i-follow-you')
    def do_i_follow_you(self, request, pk):
        profile = request.user.profile
        doing = profile.followings.filter(pk=pk).exists()
        if doing:
            return Response({'detail': 'Yes i follow you.', 'doing': True}, status=status.HTTP_200_OK)
        return Response({'detail': "No i don't follow you.", 'doing': False}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'], url_path='do-you-follow-me')
    def do_you_follow_me(self, request, pk):
        profile = request.user.profile
        doing = profile.followers.filter(pk=pk).exists()
        if doing:
            return Response({'detail': 'Yes you follow me.', 'doing': True}, status=status.HTTP_200_OK)
        return Response({'detail': "No you don't follow me.", 'doing': False}, status=status.HTTP_204_NO_CONTENT)
