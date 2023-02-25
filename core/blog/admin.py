from django.contrib import admin

from .models import Category, Post, Comment, PostLike, CommentLike, Save


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Save)
