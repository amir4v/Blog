from datetime import datetime

from django.core import validators

from rest_framework import serializers

from accounts.models import Profile
from core.utils import upload_avatar
import os
import copy


class ProfileModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.CharField(max_length=256, source='user.email', read_only=True)
    username = serializers.CharField(max_length=32, source='user.username', read_only=True)
    
    name = serializers.CharField(allow_blank=True, max_length=128)
    bio = serializers.CharField(allow_blank=True, max_length=1000)
    birth_date = serializers.DateField(allow_blank=True)
    location = serializers.CharField(allow_blank=True, max_length=64)
    status = serializers.CharField(allow_blank=True, max_length=32)
    
    profile_avatar = serializers.ImageField(write_only=True, required=False, validators=[
        validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])
    ])
    avatar = serializers.CharField(max_length=256, read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'email', 'username', 'name', 'bio', 'birth_date', 'location', 'status', 'profile_avatar', 'avatar']
        read_only_fields = ['id', 'email', 'username', 'avatar']
    
    def validate(self, attrs):
        avatar = attrs.get('profile_avatar', None)
        if avatar:
            path = upload_avatar(avatar)
            attrs['avatar'] = path
            attrs.pop('profile_avatar', None)
        
        birth_date = attrs.get('birth_date', None)
        max_year = datetime.now().year-13
        if birth_date.year < 1900 or birth_date.year > max_year:
            raise ValueError(f'Birth date year must be between 1900 and {max_year}')
        
        return super().validate(attrs)
