from uuid import uuid4
import os
from random import randint
import string
import re

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.validators import BaseValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.utils.deconstruct import deconstructible

from rest_framework_simplejwt.state import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import permissions
from rest_framework.serializers import ValidationError
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


def user_6_digit():
    return f'user{randint(100_000, 1_000_000)}'


class RangeLengthValidator(BaseValidator):
    def __init__(self, min, max, message=None):
        self.min = min
        self.max = max
        if message:
            self.message = message
    
    def __call__(self, value):
        cleaned = self.clean(value)
        MinLengthValidator(self.min).__call__(cleaned)
        MaxLengthValidator(self.max).__call__(cleaned)


class RangeValueValidator(BaseValidator):
    def __init__(self, min, max, message=None):
        self.min = min
        self.max = max
        if message:
            self.message = message
    
    def __call__(self, value):
        cleaned = self.clean(value)
        MinValueValidator(self.min).__call__(cleaned)
        MaxValueValidator(self.max).__call__(cleaned)


def validate_username(username, null=True):
    username = username.lower().strip(string.whitespace)
    
    if null and len(username) == 0:
        return None
    
    length = len(username)
    if length < 6 or length > 32:
        raise ValidationError('Username length must be between 6 and 32')
    
    if username.startswith('.') or username.startswith('_') \
        or \
        username.endswith('.') or username.endswith('_'):
            raise ValidationError('Username cannot start or end with . or _')
    
    allowed_chars = string.ascii_lowercase + string.digits + '._'
    pattern = rf'^[{allowed_chars}]{{6,32}}$'
    print(pattern)
    match = bool(re.match(pattern, username))
    if not match:
        raise ValidationError('Username must contain these allowed characters: a-z , 0-9 , . , _')
    
    return username
