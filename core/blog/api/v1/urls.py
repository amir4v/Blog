from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *


app_name = 'api-v1'


urlpatterns = []

router = DefaultRouter()

router.register('category', CategoryModelViewSet, basename='category')
router.register('post', PostModelViewSet, basename='post')
router.register('comment', CommentModelViewSet, basename='comment')
router.register('blogger', BloggerViewSet, basename='blogger')

urlpatterns += router.urls
