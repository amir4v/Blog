from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from core.utils import user_6_digit, validate_username


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        user.password = password
        #
        # if not extra_fields['is_superuser']:
        #     validate_password(password)
        # user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def create(self, *args, **kwargs):
        return self.create_user(*args, **kwargs)
    
    def create_user(self, email, password, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        extra_fields['is_verified'] = False
        extra_fields['is_active'] = False
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_verified'] = True
        extra_fields['is_active'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # password (8-64) -> .set_password('VALUE')
    # last_login
    
    USERNAME_FIELD = 'email'
    
    email = models.EmailField(
        unique=True, db_index=True, blank=False, null=False
    ) # max_length=256
    username = models.CharField(
        max_length=32, unique=True, db_index=True,
        blank=False, null=False, default=user_6_digit
    ) # length=6-32
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    def save(self, *args, **kwargs):
        if len(self.password) != 88:
            if not self.is_superuser:
                validate_password(self.password)
            self.set_password(self.password)
        
        self.username = validate_username(self.username)
        
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email
