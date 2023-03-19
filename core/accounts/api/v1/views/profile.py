from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions

from accounts.api.v1.serializers import ProfileModelSerializer
from accounts.models import Profile

User = get_user_model()


class ProfileModelViewSet(ModelViewSet):
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
