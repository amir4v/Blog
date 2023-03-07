from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions

from blog.models import *
from blog.api.v1.serializers import *


class CategoryModelViewSet(ModelViewSet):
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
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk):
        category = get_object_or_404(self.get_queryset(), pk=pk)
        posts = category.posts.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data)
