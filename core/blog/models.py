from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import Profile


User = get_user_model()


class Category(models.Model):
    pass


class Post(models.Model):
    pass


class Comment(models.Model):
    pass


class Like(models.Model):
    pass


class Save(models.Model):
    pass
