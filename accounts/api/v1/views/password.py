from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.state import api_settings
from rest_framework import permissions
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from accounts.api.v1.serializers import ForgotPasswordConfirmEmailSerializer
from core.utils import send_reset_password_email, IsNotAuthenticated

User = get_user_model()


class ForgotPasswordAPIView(APIView):
    """
    Forgot Password API View
    ------------------------
    Sends a reset password email to current user.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        send_reset_password_email(user=request.user)
        return Response(
            {'detail': 'Reset-Password email sent successfully.'},
             status=status.HTTP_200_OK
        )

class ForgotPasswordVerifyAPIView(APIView):
    """
    Forgot Password Verify API View
    -------------------------------
    Takes a token that we sent to the user for reset-password.
    
    Check the token.
    
    Empty('') the password because empty password means the user is allowed to
    reset-password.
    
    Then user can be redirect to 'register' path for reset-password
    because in 'register' path you can change your password if you've been
    saved in the database and your password is empty('').
    """
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            _token = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=[api_settings.ALGORITHM]
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
        
        user = User.objects.get(email=email)
        user.password = ''
        user.save()   
        
        login(request, user)
        # Go to 'register' route for set password.
        
        return Response(
            {
                "detail": "Now you are allow to change your password.",
                'access_token': token,
            },
            status=status.HTTP_200_OK,
        )


class ForgotPasswordConfirmGenericAPIView(GenericAPIView):
    """
    Forgot Password Generic API View
    --------------------------------
    This view is for the user that can not login to the website because he/she
    forgets him/her password.
    
    Takes an email for sending a link for resetting the password.
    
    Check existence of the email.
    
    Send a email for reset-password.
    """
    
    permission_classes = [IsNotAuthenticated]
    serializer_class = ForgotPasswordConfirmEmailSerializer    
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        user_obj = get_object_or_404(User, email=email)
        send_reset_password_email(user=user_obj)
        
        return Response(
            {'detail': 'Reset-Password-Confirm email sent successfully.'},
            status=status.HTTP_200_OK
        )
