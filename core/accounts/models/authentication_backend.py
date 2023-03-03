from django.contrib.auth.backends import ModelBackend

from .user import User


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(email=username)
            success = user.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
            return None
        # For when there is a user but the password is incorrect.
        return None
