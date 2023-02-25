from django.urls import path, include

from rest_framework.routers import SimpleRouter, DefaultRouter

from . import views


app_name = 'api-v1'

urlpatterns = [
    # path('users/', views.UserAPIView.as_view(), name='user-list'),
    # path('users/me/', views., name='user-me'),
    # path('users/profile/', views., name='user-profile'),
    #
    # path('users/reset-password/', views., name='user-reset-password'),
    #
    # path('logout/', views.logout, name='logout'),
    
    # path('users/activation/<token>/', views., name='user-activation'),
    # path('users/activation-confirm/', views., name='user-activation-confirm'),
    # ------SEPARATE------
    # path('users/reset-email/', views., name='user-reset-email'),
    # path('users/reset-email-confirm/', views., name='user-reset-email-confirm'),
    # ------SEPARATE------
    # path('users/forgot-password/', views., name='user-forgot-password'),
    # path('users/forgot-password-confirm/', views., name='user-forgot-password-confirm'),
        
    # path('jwt/create/', views., name='jwt-create'),
    # path('jwt/refresh/', views., name='jwt-refresh'),
    # path('jwt/verify/', views., name='jwt-verify'),
]

user_router = DefaultRouter()
user_router.register('users', views.UserModelViewSet, basename='users')
"""
users/
    me/
    profile/
    reset-password/
    logout/
"""

profile_router = DefaultRouter()
profile_router.register('profile', views.ProfileModelViewSet, basename='profile')

urlpatterns += user_router.urls
urlpatterns += profile_router.urls

urlpatterns += [
    path('users/activation/<str:token>/', views.UserActivationAPIView.as_view(), name='user-activation'),
    path('users/activation/confirm/', views.UserActivationConfirmAPIView.as_view(), name='user-activation-confirm'),
]
