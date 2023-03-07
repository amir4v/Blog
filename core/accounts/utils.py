from uuid import uuid4

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.state import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import permissions
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


def upload_to(file, base_dir=settings.MEDIA_ROOT, dir='', filename=None, file_extension=None):
    dir = dir.strip('/')
    name = uuid4()
    ext = ''
    filename = name + ext
    path = f'{base_dir}{dir}/{filename}'
    f = open(path, 'wb')
    f.write(file)
    f.close()
    dir = settings.MEDIA_URL.strip('/') + f'/{dir}'
    return f'{dir}/{filename}'


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user) == 'AnonymousUser'
