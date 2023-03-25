from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        """
        Overriding __init__ for changing the USERNAME_FIELD
        in the Frontend, because default it's get a 'Email' or 'Username'
        so we change it to get a text filed called 'Email or Username'
        for supporting two factor authentication.
        """
        
        super().__init__(*args, **kwargs)
        
        self.fields[self.username_field] = serializers.CharField(
            label='Email or Username',
            min_length=USERNAME_MIN_LENGTH,
            max_length=USERNAME_MAX_LENGTH
        )
