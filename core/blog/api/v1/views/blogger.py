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
from accounts.models import Profile
from accounts.api.v1.serializers import ProfileModelSerializer

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
        follow
        unfollow
        followers
        followings
        do_i_follow_you
        do_you_follow_me
    """
    
    @action(detail=False, url_path='saved-posts')
    def saved_posts(self, request):
        """Get current user's saved posts."""
        
        profile = request.user.profile
        posts = profile.posts_saved.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def categories(self, request):
        """Get current user's categories."""
        
        profile = request.user.profile
        categories = profile.categories.all()
        serializer = CategoryModelSerializer(instance=categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, url_path='category-posts')
    def category_posts(self, request, pk):
        """Get current user's category's posts."""
        
        profile = request.user.profile
        category = get_object_or_404(Category, profile=profile, pk=pk)
        posts = category.posts.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def posts(self, request):
        """Get current user's posts."""
        
        profile = request.user.profile
        posts = profile.posts.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, url_path='liked-posts')
    def liked_posts(self, request):
        """Get current user's liked posts."""
        
        profile = request.user.profile
        posts = profile.posts_liked.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, url_path='comments')
    def comments(self, request):
        """Get current user's comments."""
        
        profile = request.user.profile
        comments = profile.comments.all()
        serializer = CommentModelSerializer(instance=comments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, url_path='liked-comments')
    def liked_comments(self, request):
        """Get current user's liked comments."""
        
        profile = request.user.profile
        comments = profile.comments_liked.all()
        serializer = CommentModelSerializer(instance=comments, many=True)
        return Response(serializer.data)
    
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
        return Response(serializer.data)
    
    @action(detail=False)
    def followings(self, request):
        """Get current user's followings."""
        
        profile = request.user.profile
        fs = profile.followings.all()
        serializer = ProfileModelSerializer(instance=fs, many=True)
        return Response(serializer.data)
    
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
