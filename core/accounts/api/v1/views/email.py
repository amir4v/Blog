from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework_simplejwt.state import api_settings
from rest_framework import permissions
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from accounts.api.v1.serializers import *
from accounts.utils import send_reset_email_email


User = get_user_model()


class ResetEmailGenericAPIView(GenericAPIView):
    serializer_class = ResetEmailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @csrf_exempt
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        email = serializer.validated_data.get('email')
        user.email = email
        
        send_reset_email_email(user=user)
        
        return Response('Reset-Email email sent successfully.', status=status.HTTP_200_OK)


class ResetEmailVerifyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, token):
        try:
            _token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[api_settings.ALGORITHM]
            )
            user_id = _token.get('user_id')
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
        
        user = User.objects.get(id=user_id)
        user.email = email
        user.save()
        login(request, user)
        
        data = {
            'detail': 'Your email changed successfully.',
            'access_token': token,
        }
        return Response(data, status=status.HTTP_200_OK)
