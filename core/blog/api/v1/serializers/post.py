from django.core import validators

from rest_framework import serializers

from blog.models import *
from core.utils import upload_banner


class PostModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True, max_length=128)
    content = serializers.CharField(min_length=1)
    
    banner_image = serializers.ImageField(write_only=True, required=False, validators=[
        validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])
    ])
    banner = serializers.CharField(max_length=256, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'profile', 'category', 'banner_image', 'banner']
        read_only_fields = ['id', 'banner']
    
    def validate(self, attrs):
        user = self.context.get('request').user
        user_profile = user.profile
        profile = attrs.get('profile')
        banner = attrs.get('banner_image', None)
        category = attrs.get('category')
        
        if not user.is_superuser and user_profile != profile:
            raise serializers.ValidationError('Access denied.')
        
        if banner:
            path = upload_banner(banner)
            attrs['banner'] = path
            attrs.pop('banner_image', None)
        
        if not user_profile.categories.filter(pk=category.pk).exists():
            raise serializers.ValidationError('Access denied.')
        
        return super().validate(attrs)
