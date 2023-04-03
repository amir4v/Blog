"""
# Custom Auth User Model
USERNAME_MIN_LENGTH = 6
USERNAME_MAX_LENGTH = 32
#
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = LOGIN_URL
#
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'accounts.models.authentication_backend.CustomAuthenticationBackend',
]
"""
