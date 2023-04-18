from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from blog.models import Category
from blog.api.v1.serializers import (
    CategoryModelSerializer,
    PostModelSerializer,
)


class CategoryModelViewSet(ModelViewSet):
    """
    Category Model View Set
    -----------------------
    A user can perform these actions:
        create
        retrieve
        update
        partial_update
        destroy
        posts
    
    A admin user can perform all above actions + :
        list
    """
    
    serializer_class = CategoryModelSerializer
    
    def get_permissions(self):
        if self.action not in ['list']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        if self.action not in ['list']:
            profile = self.request.user.profile
            return Category.objects.filter(profile=profile)
        return Category.objects.all()
    
    @action(detail=True)
    def posts(self, request, pk):
        """Get the given category's posts."""
        
        category = get_object_or_404(Category, pk=pk)
        posts = category.posts.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
