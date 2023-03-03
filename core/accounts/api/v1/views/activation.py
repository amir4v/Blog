from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework_simplejwt.state import api_settings
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from accounts.api.v1.serializers import user
from accounts.api.v1.serializers import *
from accounts.utils import send_activation_email


User = get_user_model()


class UserActivationAPIView(APIView):
    def get(self, request, token):
        try:
            _token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[api_settings.ALGORITHM]
            )
            email = _token.get('email')
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has been expired!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "Token is invalid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"detail": "Token is not valid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user, created = User.objects.get_or_create(email=email)
        if user.is_verified:
            return Response(
                {"detail": "Your account is already verified."},
                status=status.HTTP_202_ACCEPTED,
            )
        user.is_verified = True
        user.is_active = True
        user.save()
        
        login(request, user)
        
        return Response(
            {
                "detail": "Your account has been verified and activated successfully.",
                'access_token': token,
            },
            status=status.HTTP_200_OK,
        )


class UserActivationConfirmGenericAPIView(GenericAPIView):
    serializer_class = UserActivationConfirmSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.data.get('email')
        user_obj = get_object_or_404(User, email=email)
        if user_obj.is_verified:
            return Response(
                {"detail": "Your account is already verified."},
                status=status.HTTP_202_ACCEPTED,
            )
        send_activation_email(user=user_obj)
        
        return Response('Confirm-Activation email sent successfully.', status=status.HTTP_200_OK)
