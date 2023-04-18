from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from accounts.models import Profile
from accounts.api.v1.serializers import ProfileModelSerializer

User = get_user_model()


class ProfileModelViewSet(ModelViewSet):
    """
    Profile Model View Set
    ----------------------
    A user can perform these actions:
        retrieve
        update
        partial_update
        follow
        unfollow
        followers
        followings
        do_i_follow_you
        do_you_follow_me
    
    A admin user can perform all above + :
        create
        destroy
        list
    """
    
    serializer_class = ProfileModelSerializer
    parser_classes = [MultiPartParser]
    
    def get_queryset(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            user = self.request.user
            return Profile.objects.filter(user=user)
        return Profile.objects.all()
        
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    @action(detail=True)
    def follow(self, request, pk):
        """Get current user follows someone."""
        
        profile = request.user.profile
        profile.followings.add(pk)
        return Response(
            {'detail': 'Successfully followed.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True)
    def unfollow(self, request, pk):
        """Get current user unfollows someone."""
        
        profile = request.user.profile
        profile.followings.remove(pk)
        return Response(
            {'detail': 'Successfully unfollowed.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False)
    def followers(self, request):
        """Get current user's followers."""
        
        profile = request.user.profile
        fs = profile.followers.all()
        serializer = ProfileModelSerializer(instance=fs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False)
    def followings(self, request):
        """Get current user's followings."""
        
        profile = request.user.profile
        fs = profile.followings.all()
        serializer = ProfileModelSerializer(instance=fs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='do-i-follow-you')
    def do_i_follow_you(self, request, pk):
        """Does current user follow the given user."""
        
        profile = request.user.profile
        you = get_object_or_404(Profile, pk=pk)
        
        doing = profile.followings.filter(pk=you).exists()
        if doing:
            return Response(
                {'detail': 'Yes i follow you.', 'doing': True},
                status=status.HTTP_200_OK
            )
        return Response(
            {'detail': "No i don't follow you.", 'doing': False},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=True, url_path='do-you-follow-me')
    def do_you_follow_me(self, request, pk):
        """Does the given user follow current user."""
        
        profile = request.user.profile
        you = get_object_or_404(Profile, pk=pk)
        
        doing = profile.followers.filter(pk=you).exists()
        if doing:
            return Response(
                {'detail': 'Yes you follow me.', 'doing': True},
                status=status.HTTP_200_OK
            )
        return Response(
            {'detail': "No you don't follow me.", 'doing': False},
            status=status.HTTP_204_NO_CONTENT
        )
