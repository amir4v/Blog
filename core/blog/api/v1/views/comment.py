from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions

from blog.models import *
from blog.api.v1.serializers import *
from accounts.api.v1.serializers.profile import ProfileModelSerializer


class CommentModelViewSet(ModelViewSet):
    serializer_class = CommentModelSerializer
    
    def get_queryset(self):
        if self.action not in ['list']:
            profile = self.request.user.profile
            return Comment.objects.filter(profile=profile)
        return Comment.objects.all()
    
    def get_permissions(self):
        if self.action not in ['list']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    @action(detail=True, methods=['get'], url_path='who-liked')
    def who_liked(self, request, pk):
        comment = get_object_or_404(self.get_queryset(), pk=pk)
        profiles = comment.who_liked.all()
        serializer = ProfileModelSerializer(instance=profiles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def like(self, request, pk):
        comment = get_object_or_404(self.get_queryset(), pk=pk)
        profile = request.user.profile
        profile.comments_liked.add(comment)
        return Response('Liked successfully.', status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def unlike(self, request, pk):
        comment = get_object_or_404(self.get_queryset(), pk=pk)
        profile = request.user.profile
        profile.comments_liked.remove(comment)
        return Response('UnLiked successfully.', status=status.HTTP_200_OK)
