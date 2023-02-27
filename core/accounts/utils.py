from django.core.mail import send_mail
from django.conf import settings

from rest_framework_simplejwt.state import api_settings
from rest_framework_simplejwt.tokens import AccessToken
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError


def get_activation_token(user):
    access_token = AccessToken()
    access_token.payload['email'] = user.email
    return str(access_token)


def send_activation_email(user):
    address = 'http://127.0.0.1:8000/accounts/api/v1/users/activation'
    token = get_activation_token(user)
    link = f'{address}/{token}/'
    send_mail(
        'Activation Link',
        f"Link: {link}",
        'admin.admin.admin',
        [user.email,],
        fail_silently=False,
    )

"""
from django.conf import settings
from rest_framework_simplejwt.state import api_settings
jwt.encode()
def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[api_settings.ALGORITHM]
            )
            user_id = token.get("user_id")
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

        user = get_object_or_404(User, pk=user_id)
        if user.is_verified:
            return Response(
                {"detail": "Your account is already verified and activated."},
                status=status.HTTP_202_ACCEPTED,
            )
        user.is_verified = True
        user.is_active = True
        user.save()

        return Response(
            {
                "detail": "Your account has been verified and activated successfully."
            },
            status=status.HTTP_200_OK,
        )
        
        

"""