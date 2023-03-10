from rest_framework import serializers

from blog.models import *
from core.utils import RangeLengthValidator


class CategoryModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=1, max_length=128)
    
    class Meta:
        model = Category
        fields = ['name', 'profile']
    
    def validate(self, attrs):
        user = self.context.get('request').user
        user_profile = user.profile
        profile = attrs.get('profile')
        
        if not user.is_superuser and user_profile != profile:
            raise serializers.ValidationError('Access denied.')
        
        return super().validate(attrs)
