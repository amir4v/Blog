from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from .user import User


class Profile(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True, default=None)
    bio = models.TextField(blank=True, null=True, default=None)
    birth_date = models.DateField(blank=True, null=True, default=None)
    location = models.CharField(max_length=64, blank=True, null=True, default=None)
    status = models.CharField(max_length=32, blank=True, null=True, default=None) # emoji
    avatar = models.CharField(max_length=256, blank=True, null=True, default=None)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    followers = models.ManyToManyField('Profile', related_name='followings')
    
    def __str__(self):
        return f"{self.user} - {self.name or ':)'}"


@receiver(post_save, sender=User)
def user_created(sender, instance, created, *args, **kwargs):
    """This is for create a profile for the just created user."""
    
    if created:
        Profile.objects.create(user=instance)
