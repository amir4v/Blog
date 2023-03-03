from django.core.mail import send_mail
from django.conf import settings

from rest_framework_simplejwt.state import api_settings
from rest_framework_simplejwt.tokens import AccessToken
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError


def get_activation_token(user):
    access_token = AccessToken()
    access_token.payload['user_id'] = user.id or None
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


def send_reset_password_email(user):
    address = 'http://127.0.0.1:8000/accounts/api/v1/users/forgot-password-verify'
    token = get_activation_token(user)
    link = f'{address}/{token}/'
    send_mail(
        'Reset-Password Link',
        f"Link: {link}",
        'admin.admin.admin',
        [user.email,],
        fail_silently=False,
    )


def send_reset_email_email(user):
    address = 'http://127.0.0.1:8000/accounts/api/v1/users/reset-email-verify'
    token = get_activation_token(user)
    link = f'{address}/{token}/'
    send_mail(
        'Reset-Email Link',
        f"Link: {link}",
        'admin.admin.admin',
        [user.email,],
        fail_silently=False,
    )
