from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions

from blog.models import Comment
from blog.api.v1.serializers import CommentModelSerializer
from accounts.api.v1.serializers.profile import ProfileModelSerializer


class CommentModelViewSet(ModelViewSet):
    """
    Comment Model View Set
    ----------------------
    A user can perform these actions:
        create
        retrieve
        update
        partial_update
        destroy
        who_liked
        like
        unlike
    
    A admin user can perform all above actions + :
        list
    """
    
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
    
    @action(detail=True, url_path='who-liked')
    def who_liked(self, request, pk):
        """Get profiles that liked the given comment."""
        
        comment = get_object_or_404(Comment, pk=pk)
        profiles = comment.who_liked.all()
        serializer = ProfileModelSerializer(instance=profiles, many=True)
        return Response(serializer.data)
    
    @action(detail=True)
    def like(self, request, pk):
        """Like the given comment."""
        
        comment = get_object_or_404(Comment, pk=pk)
        profile = request.user.profile
        profile.comments_liked.add(comment)
        return Response('Liked successfully.', status=status.HTTP_200_OK)
    
    @action(detail=True)
    def unlike(self, request, pk):
        """Un-Like the given comment."""
        
        comment = get_object_or_404(Comment, pk=pk)
        profile = request.user.profile
        profile.comments_liked.remove(comment)
        return Response('UnLiked successfully.', status=status.HTTP_200_OK)
