from rest_framework import serializers

from accounts.models import Profile
from accounts.utils import upload_avatar
import os
import copy


class ProfileModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_email = serializers.CharField(max_length=256, source='user.email', read_only=True)
    
    profile_avatar = serializers.ImageField(write_only=True, required=False)
    avatar = serializers.CharField(max_length=256, read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'name', 'bio', 'birth_date', 'location', 'status', 'profile_avatar', 'avatar', 'user_id', 'user_email']
        read_only_fields = ['id', 'user_id', 'user_email']
    
    def validate(self, attrs):
        avatar = attrs.get('profile_avatar', None)
        if avatar:
            path = upload_avatar(avatar)
            attrs['avatar'] = path
            attrs.pop('profile_avatar', None)
        return super().validate(attrs)
