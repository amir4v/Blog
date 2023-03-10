from django.contrib.auth import get_user_model, logout as Logout, login as Login

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import permissions

from accounts.api.v1.serializers import *
from accounts.utils import send_activation_email, IsNotAuthenticated


User = get_user_model()


class UserModelViewSet(ModelViewSet):
    def get_queryset(self):
        if self.action in ['pre_register']:
            return None
        if self.action in ['register', 'me', 'profile', 'reset_password', 'logout']:
            pk = self.request.user.pk
            return User.objects.filter(pk=pk)
        return User.objects.all()
    
    def get_permissions(self):
        if self.action in ['pre_register']:
            return [IsNotAuthenticated()]
        if self.action in ['register', 'me', 'profile', 'reset_password', 'logout']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    def get_serializer_class(self):
        if self.action == 'pre_register':
            return ActivationEmailModelSerializer
        if self.action == 'register':
            return FirstTimeSetPasswordSerializer
        if self.action == 'profile':
            return ProfileModelSerializer
        if self.action == 'reset_password':
            return ResetPasswordSerializer
        if self.action == 'reset_username':
            return ResetUsernameSerializer
        return UserModelSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """PUT and PATCH are not allowed."""
        return Response({'detail': 'Not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
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
        data = self.get_serializer(instance=request.user.profile).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        Logout(request)
        return Response('Password changed successfully.', status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='reset-username')
    def reset_username(self, request):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response('Username changed successfully.', status=status.HTTP_200_OK)
    
    @action(detail=False)
    def logout(self, request):
        Logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
