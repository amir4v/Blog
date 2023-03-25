from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()


class Profile(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True, default=None)
    avatar = models.CharField(max_length=256, blank=True, null=True, default=None)
    
    # created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    followers = models.ManyToManyField('Profile', related_name='followings')
    
    def __str__(self):
        return f"{self.user} - {self.name or ':)'}"


@receiver(post_save, sender=User)
def user_created(sender, instance, created, *args, **kwargs):
    """This is for create a profile for the just created user."""
    
    if created:
        Profile.objects.create(user=instance)
