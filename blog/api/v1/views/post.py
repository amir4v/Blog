from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser

from blog.models import Post
from blog.api.v1.serializers import PostModelSerializer, CommentModelSerializer
from accounts.api.v1.serializers.profile import ProfileModelSerializer


class PostModelViewSet(ModelViewSet):
    """
    Post Model View Set
    -------------------
    A user can perform these actions:
        create
        retrieve
        update
        partial_update
        destroy
        who_liked
        comments
        like
        unlike
        save
        unsave
    
    A admin user can perform all above actions + :
        list
    """
    
    serializer_class = PostModelSerializer
    parser_classes = [MultiPartParser]
    
    def get_permissions(self):
        if self.action not in ['list']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        if self.action not in ['list']:
            profile = self.request.user.profile
            return Post.objects.filter(profile=profile)
        return Post.objects.all()
    
    def get_object(self):
        """Overriding for increasing the seen field."""
        
        obj = super().get_object()
        obj.seen += 1
        obj.save()
        return obj
    
    @action(detail=True, url_path='who-liked')
    def who_liked(self, request, pk):
        """Get users/profiles that liked the given post."""
        
        post = get_object_or_404(Post, pk=pk)
        profiles = post.who_liked.all()
        serializer = ProfileModelSerializer(instance=profiles, many=True)
        return Response(serializer.data)
    
    @action(detail=True)
    def comments(self, request, pk):
        """Get the given post's comments."""
        
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        serializer = CommentModelSerializer(instance=comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True)
    def like(self, request, pk):
        """Current user likes the given post."""
        
        profile = request.user.profile
        post = get_object_or_404(Post, pk=pk)
        profile.posts_liked.add(post)
        return Response('Liked successfully.', status=status.HTTP_200_OK)
    
    @action(detail=True)
    def unlike(self, request, pk):
        """Current user unlikes the given post."""
        
        profile = request.user.profile
        post = get_object_or_404(Post, pk=pk)
        profile.posts_liked.remove(post)
        return Response('UnLiked successfully.', status=status.HTTP_200_OK)
    
    @action(detail=True)
    def save(self, request, pk):
        """Current user saves the given post."""
        
        profile = request.user.profile
        post = get_object_or_404(Post, pk=pk)
        profile.posts_saved.add(post)
        return Response('Saved successfully.', status=status.HTTP_200_OK)
    
    @action(detail=True)
    def unsave(self, request, pk):
        """Current user unsaves the given post."""
        
        profile = request.user.profile
        post = get_object_or_404(Post, pk=pk)
        profile.posts_saved.remove(post)
        return Response('UnSaved successfully.', status=status.HTTP_200_OK)
