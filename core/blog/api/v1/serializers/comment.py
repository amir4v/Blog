from rest_framework import serializers

from blog.models import *


class CommentModelSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(min_length=1, max_length=1000)
    
    class Meta:
        model = Comment
        fields = ['comment', 'profile', 'post']
    
    def validate(self, attrs):
        user = self.context.get('request').user
        user_profile = user.profile
        profile = attrs.get('profile')
        
        if not user.is_superuser and user_profile != profile:
            raise serializers.ValidationError('Access denied.')
        
        return super().validate(attrs)
