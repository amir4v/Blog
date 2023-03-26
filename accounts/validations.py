import string
import re

from rest_framework.serializers import ValidationError

from accounts.models.config import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH


def validate_username(username, null=True):
    """
    Custom username validator.
    first checking the length of the username.
    username cannot start or end with '.' .
    allowed characters are a-z and 0-9 and . and _ with the given length limit.
    username at least must have a alphabetic character or a number.
    then returns the username.
    """
    
    username = username.lower().strip(string.whitespace)
    
    if null and len(username) == 0:
        return None
    
    length = len(username)
    if length < USERNAME_MIN_LENGTH or length > USERNAME_MAX_LENGTH:
        raise ValidationError(f'Username length must be between {USERNAME_MIN_LENGTH} and {USERNAME_MAX_LENGTH}')
    
    if username.startswith('.') or username.endswith('.'):
        raise ValidationError('Username cannot start or end with . ')
    
    allowed_chars = string.ascii_lowercase + \
                    string.digits + \
                    '._'
    pattern = rf'^[{allowed_chars}]' + \
              rf'{{' + \
              rf'{USERNAME_MIN_LENGTH},{USERNAME_MAX_LENGTH}' + \
              rf'}}$'
    match = bool(re.match(pattern, username))
    if not match:
        raise ValidationError('Username must contain these allowed characters: a-z , 0-9 , . , _')
    
    allowed_chars = string.ascii_lowercase + \
                    string.digits
    pattern = rf'^.*[{allowed_chars}]+.*$'
    match = bool(re.match(pattern, username))
    if not match:
        raise ValidationError('Username at least must contain an alphabetic character(a-z) or a number(0-9).')
    
    return username
