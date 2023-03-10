from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from accounts.api.v1.serializers.profile import ProfileModelSerializer
from core.utils import validate_username


User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, max_length=32)
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    profile = ProfileModelSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'profile']
        read_only_fields = ['profile']
    
    def validate(self, attrs):
        username = validate_username(attrs.get('username'))
        attrs['username'] = username
        return super().validate(attrs)


class LoginModelSerializer(serializers.ModelSerializer):
    email_or_username = serializers.CharField(max_length=256)
    
    class Meta:
        model = User
        fields = ['email_or_username', 'password']
    
    def validate(self, attrs):
        self.user = authenticate(self.context.get('request'), attrs.get('email_or_username'), attrs.get('password'))
        attrs.pop('email_or_username', None)
        return super().validate(attrs)
    
    @property
    def user(self):
        return self.user


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=64)
    new_password = serializers.CharField(min_length=8, max_length=64)
    confirm_new_password = serializers.CharField(min_length=8, max_length=64)
    
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
            raise ValidationError('Old-Password is incorrect!')
        
        return super().validate(attrs)


class ResetUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField(min_length=6, max_length=32)
    
    def validate(self, attrs):
        username = validate_username(attrs.get('username'))
        attrs['username'] = username
        user = self.context.get('user')
        user.username = username
        user.save()
        return super().validate(attrs)


class FirstTimeSetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8, max_length=64)
    confirm_new_password = serializers.CharField(min_length=8, max_length=64)
    
    def validate(self, attrs):
        user = self.context.get('user')
        
        if user.password:
            raise ValidationError("You've already set password!")
        
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise ValidationError('Passwords do not match!')
        
        user.set_password(new_password)
        user.save()
                
        return super().validate(attrs)
