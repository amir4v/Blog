from django.db import models

from accounts.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='categories')
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True,
                             default=None)
    content = models.TextField(blank=False, null=False)
    banner = models.CharField(max_length=256, blank=True, null=True,
                              default=None)
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='posts')
    
    seen = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    who_saved = models.ManyToManyField(Profile, related_name='posts_saved')
    who_liked = models.ManyToManyField(Profile, related_name='posts_liked')
    
    def __str__(self):
        if self.title:
            return self.title[:64] + '...'
        else:
            return self.content[:64] + '...'


class Comment(models.Model):
    comment = models.CharField(max_length=1000, blank=False, null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    
    who_liked = models.ManyToManyField(Profile, related_name='comments_liked')
    
    def __str__(self):
        return self.comment[:64] + '...'
