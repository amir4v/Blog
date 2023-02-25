from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from accounts.api.v1.serializers.profile import ProfileSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = ['email', 'password', 'profile']
        read_only_fields = ['profile']


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    confirm_new_password = serializers.CharField(max_length=128)
    
    def validate(self, attrs):
        user = self.context.get('user')
        
        old_password = attrs.get('old_password')
        
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')
        
        if new_password != confirm_new_password:
            raise ValidationError('Passwords do not match!')
        
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
        else:
            raise ValidationError('The Old-Password is incorrect!')
        
        return super().validate(attrs)
