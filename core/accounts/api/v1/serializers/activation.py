from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class ActivationEmailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UserActivationConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
