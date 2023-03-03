from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from blog.models import *
from blog.api.v1.serializers import *
from accounts.api.v1.serializers.profile import ProfileModelSerializer


class CommentModelViewSet(ModelViewSet):
    serializer_class = CommentModelSerializer
    queryset = Comment.objects.all()
    
    @action(detail=True, methods=['get'], url_path='who-liked')
    def who_liked(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        profiles = comment.who_liked.all()
        serializer = ProfileModelSerializer(instance=profiles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def like(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        profile = request.user.profile
        profile.comments_liked.add(comment)
        return Response('Liked successfully.', status=status.HTTP_200_OK)
