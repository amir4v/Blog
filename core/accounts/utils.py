from uuid import uuid4
import os

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.state import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import permissions
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from celery import shared_task


def get_activation_token(user):
    access_token = AccessToken()
    access_token.payload['user_id'] = user.id or None
    access_token.payload['email'] = user.email
    return str(access_token)


@shared_task
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


@shared_task
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


@shared_task
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


def upload(uploaded_file, dir):
    dir = ['/media'] + dir
    
    name = str(uuid4())
    ext = uploaded_file.name.split('.')[-1] or 'unknown'
    filename = f'{name}.{ext}'
    
    path = os.path.join(settings.MEDIA_ROOT, *dir[1:], filename)
    f = open(path, 'wb')
    file_bytes = uploaded_file.file.read()
    f.write(file_bytes)
    f.close()
    
    dir.append(filename)
    path = '/'.join(dir)
    return path


@shared_task
def upload_avatar(avatar):
    dir = ['user', 'profile', 'avatar']
    path = upload(avatar, dir)
    return path


@shared_task
def upload_banner(banner):
    dir = ['post', 'banner']
    path = upload(banner, dir)
    return path


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user) == 'AnonymousUser'
