from django.conf import settings

if hasattr(settings, 'USERNAME_MIN_LENGTH'):
    USERNAME_MIN_LENGTH = settings.USERNAME_MIN_LENGTH
else:
    USERNAME_MIN_LENGTH = 6

if hasattr(settings, 'USERNAME_MAX_LENGTH'):
    USERNAME_MAX_LENGTH = settings.USERNAME_MAX_LENGTH
else:
    USERNAME_MAX_LENGTH = 32
