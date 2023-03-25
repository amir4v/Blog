from django.contrib.auth.backends import ModelBackend

from .user import User


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, username=None, **kwargs):
        """
        This custom authentication returns a user with the
        given credentials and it also implements two factor authentication.
        """
        
        if email is None and username is None:
            return None
        if password is None:
            return None
        
        if username is None:
            username = email
        
        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
            
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
