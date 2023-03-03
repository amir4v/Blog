from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from blog.models import *
from blog.api.v1.serializers import *


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        posts = category.posts.all()
        serializer = PostModelSerializer(instance=posts, many=True)
        return Response(serializer.data)
