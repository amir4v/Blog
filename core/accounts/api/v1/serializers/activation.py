from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from accounts.api.v1.serializers.profile import ProfileModelSerializer


User = get_user_model()


class ActivationEmailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UserActivationConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
