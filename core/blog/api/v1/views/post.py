from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from blog.models import *
from blog.api.v1.serializers import *
from accounts.api.v1.serializers.profile import ProfileModelSerializer


class PostModelViewSet(ModelViewSet):
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()
        
    @action(detail=True, methods=['get'], url_path='who-liked')
    def who_liked(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        profiles = post.who_liked.all()
        serializer = ProfileModelSerializer(instance=profiles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        serializer = CommentModelSerializer(instance=comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def like(self, request, pk):
        profile = request.user.profile
        post = get_object_or_404(Post, pk=pk)
        profile.posts_liked.add(post)
        return Response('Liked successfully.', status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def save(self, request, pk):
        profile = request.user.profile
        post = get_object_or_404(Post, pk=pk)
        profile.posts_saved.add(post)
        return Response('Saved successfully.', status=status.HTTP_200_OK)
