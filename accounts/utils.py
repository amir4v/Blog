from random import randint
from uuid import uuid4
import os

from django.core.mail import send_mail
from django.conf import settings

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.serializers import ValidationError
from rest_framework.permissions import BasePermission
from celery import shared_task
from PIL import Image

if hasattr(settings, 'HOST'):
    HOST = settings.HOST
else:
    HOST = 'http://127.0.0.1:8000'


def user_6_digit():
    """Default value for username."""
    
    return f'user{randint(100_000, 1_000_000)}'


def get_activation_token(user):
    """
    Returns a jwt access token for the given user
    and manually adding 'user_id' (if there is one because sometimes we
        send an email to an AnonymousUser and that user does not has an ID yet)
    and 'email' to the jwt token payload for the receiver.
    """
    
    access_token = AccessToken()
    access_token.payload['user_id'] = user.id or None
    access_token.payload['email'] = user.email
    return str(access_token)


@shared_task
def send_activation_email(user):
    """
    Send an account activation email link to the given user.
    """
    
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
    """
    Send a reset password email link to the given user.
    """
    
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
    """
    Send a reset-email email link to the given user.
    """
    
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
    """
    Takes a file and a size in byte
    and checks if the file size is in the given size range.
    
    then checks if file image size(width, height) is at least
    10px both width and height.
    """
    
    file_size = file.size
    min_size, max_size, error_message = size
    if file_size < min_size or file_size > max_size:
        raise ValidationError(error_message)
    
    x, y = file.image.size
    if x < 10 or y < 10:
        raise ValidationError('Image resolution at least must be Width: 10px, Height: 10px')


def upload(uploaded_file, dir, size, res=None, thumbnail_size=None):
    """
    Uploads the given uploaded file to the given directory with
    the given size(in byte) and res(width and height).
    also you can give a thumbnail size if you want to create a thumbnail too.
    and then return the uploaded file path.
    """
    
    check_file_size(uploaded_file, size)
    
    dir = ['/media'] + dir
    
    name = str(uuid4())
    ext = uploaded_file.name.split('.')[-1] or 'unknown'
    filename = f'{name}.{ext}'
    path = os.path.join(settings.MEDIA_ROOT, *dir[1:], filename)
    """
    MEDIA_ROOT_BASE_PATH + folders path (minus the first folder because
    with giving MEDIA_ROOT we already gave /media/ part of path) + filename .
    """
    
    image = Image.open(uploaded_file.file)
    
    if res:
        """If we want to resize the image."""
        image.resize(res).save(path)
    else:
        """Otherwise we just save it."""
        image.save(path)
    
    if thumbnail_size:
        """If want a thumbnail we resize the image and save it."""
        image = image.resize(thumbnail_size)
        thumbnail_path = os.path.join(
                settings.MEDIA_ROOT,
                *dir[1:], """When we gave MEDIA_ROOT_BASE_PATH then we
                             don't need the first folder because MEDIA_ROOT
                             already gives /media/ folder path."""
                'thumbnail',
                filename
            )
        image.save(thumbnail_path)
    
    dir.append(filename)
    path = '/'.join(dir)
    return path


@shared_task
def upload_avatar(avatar):
    """
    Uploading avatar image with a min filesize and a max file size.
    also we can add res(width, height) to resize
    and thumbnail res to make a one.
    """
    
    min_size = 1024
    max_size = 1 * 1024 * 1024
    error_message = f'File size must be between {min_size//1024}KB, {max_size//1024//1024}MB.'
    size = min_size, max_size, error_message
    
    dir = ['user', 'profile', 'avatar']
    path = upload(avatar, dir, size, thumbnail_size=(100, 100))
    return path


class IsNotAuthenticated(BasePermission):
    """
    Check if the user is not authenticated.
    """
    
    def has_permission(self, request, view):
        return str(request.user) == 'AnonymousUser'
