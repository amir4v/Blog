from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class ResetEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    confirm_new_email = serializers.EmailField()
    
    def validate(self, attrs):
        new_email = attrs.get('new_email')
        confirm_new_email = attrs.get('new_confirm_email')
        
        if new_email != confirm_new_email:
            raise serializers.ValidationError('Emails do not match!')
        
        if User.objects.filter(email=new_email).exists():
            raise serializers.ValidationError('Email already exists!')
        
        return super().validate(attrs)
