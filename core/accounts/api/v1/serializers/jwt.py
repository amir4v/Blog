from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(label='Email or Username',
                                                                 min_length=settings.USERNAME_MIN_LENGTH,
                                                                 max_length=settings.USERNAME_MAX_LENGTH)
