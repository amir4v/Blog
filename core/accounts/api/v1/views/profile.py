from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action

from accounts.api.v1.serializers import *
from accounts.models import Profile


User = get_user_model()


class ProfileModelViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
