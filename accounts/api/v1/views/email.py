from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.state import api_settings
from rest_framework import permissions
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import jwt

from accounts.api.v1.serializers import *
from core.utils import send_reset_email_email

User = get_user_model()


class ResetEmailGenericAPIView(GenericAPIView):
    """
    Reset Email Generic API View
    ----------------------------
    Takes a new email and checks email not be exist and
    sends a link to that new email for verifying.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetEmailSerializer
    
    @csrf_exempt
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        email = serializer.validated_data.get('email')
        user.email = email
        
        send_reset_email_email(user=user)
        
        return Response(
            {'detail': 'Reset-Email email sent successfully.'},
            status=status.HTTP_200_OK
        )


class ResetEmailVerifyAPIView(APIView):
    """
    Reset Email Verify API View
    ---------------------------
    Takes a token and checks the token and then will set the new email.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, token):
        try:
            _token = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=[api_settings.ALGORITHM]
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
