from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class ResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirm_email = serializers.EmailField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        confirm_email = attrs.get('confirm_email')
        
        if email != confirm_email:
            raise serializers.ValidationError('Emails do not match!')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists!')
        
        return super().validate(attrs)
