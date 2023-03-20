from uuid import uuid4
import os
from random import randint
import string
import re

from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import (
    BaseValidator,
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import permissions
from rest_framework.serializers import ValidationError
from celery import shared_task
from PIL import Image

HOST = 'http://127.0.0.1:8000'


def get_activation_token(user):
    access_token = AccessToken()
    access_token.payload['user_id'] = user.id or None
    access_token.payload['email'] = user.email
    return str(access_token)


@shared_task
def send_activation_email(user):
    address = f'{HOST}/accounts/api/v1/user/activation'
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
    address = f'{HOST}/accounts/api/v1/user/forgot-password-verify'
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
    address = f'{HOST}/accounts/api/v1/user/reset-email-verify'
    token = get_activation_token(user)
    link = f'{address}/{token}/'
    send_mail(
        'Reset-Email Link',
        f"Link: {link}",
        'admin.admin.admin',
        [user.email,],
        fail_silently=False,
    )


def check_file_size(file, size):
    file_size = file.size
    min_size, max_size, error_message = size
    if file_size < min_size or file_size > max_size:
        raise ValidationError(error_message)
    
    x, y = file.image.size
    if x < 10 or y < 10:
        raise ValidationError('Image resolution at least must be Width: 10px, Height: 10px')


def upload(uploaded_file, dir, size, res=None, thumbnail_size=None):
    check_file_size(uploaded_file, size)
    
    dir = ['/media'] + dir
    
    name = str(uuid4())
    ext = uploaded_file.name.split('.')[-1] or 'unknown'
    filename = f'{name}.{ext}'
    path = os.path.join(settings.MEDIA_ROOT, *dir[1:], filename)
    
    image = Image.open(uploaded_file.file)
    
    if res:
        image.resize(res).save(path)
    else:
        image.save(path)
    
    if thumbnail_size:
        image = image.resize(thumbnail_size)
        thumbnail_path = os.path.join(
                settings.MEDIA_ROOT,
                *dir[1:],
                'thumbnail',
                filename
            )
        image.save(thumbnail_path)
    
    dir.append(filename)
    path = '/'.join(dir)
    return path


@shared_task
def upload_avatar(avatar):
    min_size = 1024
    max_size = 1 * 1024 * 1024
    error_message = f'File size must be between {min_size//1024}KB, {max_size//1024//1024}MB.'
    size = min_size, max_size, error_message
    
    dir = ['user', 'profile', 'avatar']
    path = upload(avatar, dir, size, thumbnail_size=(100, 100))
    return path


@shared_task
def upload_banner(banner):
    min_size = 1024
    max_size = 1 * 1024 * 1024
    error_message = f'File size must be between {min_size//1024}KB, {max_size//1024//1024}MB.'
    size = min_size, max_size, error_message
    
    dir = ['post', 'banner']
    path = upload(banner, dir, size)
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
    if length < settings.USERNAME_MIN_LENGTH or length > settings.USERNAME_MAX_LENGTH:
        raise ValidationError(f'Username length must be between {settings.USERNAME_MIN_LENGTH} and {settings.USERNAME_MAX_LENGTH}')
    
    if username.startswith('.') or username.endswith('.'):
        raise ValidationError('Username cannot start or end with . ')
    
    allowed_chars = string.ascii_lowercase + \
                    string.digits + \
                    '._'
    pattern = rf'^[{allowed_chars}]' + \
              rf'{{' + \
              rf'{settings.USERNAME_MIN_LENGTH},{settings.USERNAME_MAX_LENGTH}' + \
              rf'}}$'
    match = bool(re.match(pattern, username))
    if not match:
        raise ValidationError('Username must contain these allowed characters: a-z , 0-9 , . , _')
    
    return username
