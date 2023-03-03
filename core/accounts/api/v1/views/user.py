from django.contrib.auth import get_user_model, logout as Logout, login as Login

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from accounts.api.v1.serializers import *
from accounts.utils import send_activation_email


User = get_user_model()


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'reset_password':
            return ResetPasswordSerializer
        if self.action == 'pre_register':
            return ActivationEmailModelSerializer
        if self.action == 'register':
            return FirstTimeSetPasswordSerializer
        return UserModelSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='pre-register')
    def pre_register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.email = serializer.data.get('email')
        send_activation_email(user=user)
        
        return Response('Activation email sent successfully.', status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        
        return Response('Successfully set new password.', status=status.HTTP_200_OK)
    
    @action(detail=False)
    def me(self, request):
        data = self.get_serializer(instance=request.user).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False)
    def profile(self, request):
        data = ProfileModelSerializer(instance=request.user.profile).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response('Password changed successfully.', status=status.HTTP_200_OK)
    
    @action(detail=False)
    def logout(self, request):
        Logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
