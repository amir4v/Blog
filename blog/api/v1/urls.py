from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api-v1'

urlpatterns = []

router = DefaultRouter()

router.register('category', views.CategoryModelViewSet, basename='category')
router.register('post', views.PostModelViewSet, basename='post')
router.register('comment', views.CommentModelViewSet, basename='comment')
router.register('blogger', views.BloggerViewSet, basename='blogger')
router.register('pages', views.PagesViewSet, basename='pages')

urlpatterns += router.urls
