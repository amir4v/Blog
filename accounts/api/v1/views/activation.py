from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.state import api_settings
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import jwt

from accounts.api.v1.serializers import EmailUserActivationModelSerializer
from accounts.utils import send_activation_email, IsNotAuthenticated

User = get_user_model()


class UserActivationAPIView(APIView):
    """
    User Activation API View
    ------------------------
    In pre-register when a client gives an email for register, we send an email
    to that email with a link for verifying which that link comes here.
    
    Takes a token that we sent to the user for verifying given email.
    
    Check the token.
    
    Empty('') the password because empty password means the user is allowed to
    set a new password.
    
    Then user can be redirect to 'register' path for set a new password
    because in 'register' path you can set a new password if you've been
    saved in the database and your password is empty('').
    """
    
    permission_classes = [IsNotAuthenticated]

    def get(self, request, token):
        try:
            _token = jwt.decode(
                jwt=token, key=settings.SECRET_KEY,
                algorithms=[api_settings.ALGORITHM]
            )
            email = _token.get("email")
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
        user.password = ''
        user.is_verified = True
        user.is_active = True
        user.save()

        login(request, user)
        # Go to 'register' route for set password.

        return Response(
            {
                "detail": "Your account has been verified and activated successfully.",
                "access_token": token,
            },
            status=status.HTTP_200_OK,
        )


class UserActivationConfirmGenericAPIView(GenericAPIView):
    pass

    """
    User Activation Confirmation Generic API View
    ---------------------------------------------
    This view is for when a user in pre-register gave an email and we performed
    sending a verification email but the email didn't send and the user want
    us to send a verification email again.
    
    Takas an email that must be exist.
    
    If the user exists, it must not be verified because if it's verified that
    means the user performed this action completely.
    
    Send a link again for verifying the user account.
    """
    
    serializer_class = EmailUserActivationModelSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = get_object_or_404(User, email=email)
        if user.is_verified:
            return Response(
                {"detail": "Your account is already verified."},
                status=status.HTTP_202_ACCEPTED,
            )
        send_activation_email(user=user)

        return Response(
            {"detail": "Activation-Confirm email sent successfully."},
            status=status.HTTP_200_OK,
        )
