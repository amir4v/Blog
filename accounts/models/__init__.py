from django.conf import settings

from .user import User
from .profile import Profile

if settings.get('USERNAME_MIN_LENGTH', None):
    USERNAME_MIN_LENGTH = settings.USERNAME_MIN_LENGTH
else:
    USERNAME_MIN_LENGTH = 6

if settings.get('USERNAME_MAX_LENGTH', None):
    USERNAME_MAX_LENGTH = settings.USERNAME_MAX_LENGTH
else:
    USERNAME_MAX_LENGTH = 32
