from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from accounts.api.v1.serializers.profile import ProfileModelSerializer


User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    profile = ProfileModelSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'profile']
        read_only_fields = ['profile']


class LoginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def validate(self, attrs):
        super_validate = super().validate(attrs)
        
        user = get_object_or_404(User, email=attrs.get('email'))
        user.check_password(attrs.get('password'))
        self.user = user
        
        return super_validate
    
    @property
    def user(self):
        return self.user


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


class FirstTimeSetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)
    confirm_new_password = serializers.CharField(max_length=128)
    
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
