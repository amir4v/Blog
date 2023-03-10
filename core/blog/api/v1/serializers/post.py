from django.core import validators

from rest_framework import serializers

from blog.models import *
from core.utils import upload_banner


class PostModelSerializer(serializers.ModelSerializer):
    banner_image = serializers.ImageField(write_only=True, required=False, validators=[
        validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])
    ])
    banner = serializers.CharField(max_length=256, read_only=True)
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'profile', 'category', 'banner_image', 'banner', 'absolute_url']
    
    def validate(self, attrs):
        banner = attrs.get('banner_image', None)
        if banner:
            path = upload_banner(banner)
            attrs['banner'] = path
            attrs.pop('banner_image', None)
        return super().validate(attrs)
    
    def get_absolute_url(self, post):
        return 'http://127.0.0.1:8000' + post.banner
