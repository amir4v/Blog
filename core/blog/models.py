from django.db import models

from accounts.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='categories')
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True, default=None)
    content = models.TextField(blank=False, null=False)
    banner = models.ImageField(upload_to='media/post/banner', blank=True, null=True, default=None)
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        if self.title:
            return self.title[:64] + '...'
        else:
            return self.content[:64] + '...'


class Comment(models.Model):
    comment = models.CharField(max_length=1024, blank=False, null=False)
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return self.comment[:64] + '...'


class PostLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='who_liked')
    
    def __str__(self):
        return f'{self.profile} -> {self.post}'


class CommentLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='who_liked')
    
    def __str__(self):
        return f'{self.profile} -> {self.comment}'


class Save(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saved')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='who_saved')
    
    def __str__(self):
        return f'{self.profile} -> {self.post}'
