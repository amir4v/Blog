from django.urls import path, include

from rest_framework.routers import SimpleRouter, DefaultRouter

from . import views


app_name = 'api-v1'

urlpatterns = [
    # users/
    # users/me/
    # users/profile/
    # users/reset-password/
    # users/activation/<token>/
    # users/activation-confirm/
    # logout/
    # ------SEPARATE------
    # users/forgot-password/
    # users/forgot-password-confirm/
    # ------SEPARATE------
    # users/reset-email/
    # users/reset-email-confirm/
    # ------SEPARATE------
    # jwt/create/
    # jwt/refresh/
    # jwt/verify/
]

urlpatterns += [
    path('users/activation/<str:token>/', views.UserActivationAPIView.as_view(), name='user-activation'),
    path('users/activation-confirm/', views.UserActivationConfirmGenericAPIView.as_view(), name='user-activation-confirm'),
    
    path('users/forgot-password/', views.ForgotPasswordAPIView.as_view(), name='user-forgot-password'),
    # path('users/forgot-password-confirm/', views.ForgotPasswordConfirmGenericAPIView.as_view(), name='user-forgot-password-confirm'),
    
    # path('users/reset-email/', views.ResetEmailAPIView.as_view(), name='user-reset-email'),
    # path('users/reset-email-confirm/', views.ResetEmailConfirmGenericAPIView.as_view(), name='user-reset-email-confirm'),
]

user_router = DefaultRouter()
user_router.register('users', views.UserModelViewSet, basename='users')
"""
users/
    pre-register/
    register/
    me/
    profile/
    reset-password/
    logout/
"""

profile_router = DefaultRouter()
profile_router.register('profile', views.ProfileModelViewSet, basename='profile')

urlpatterns += user_router.urls
urlpatterns += profile_router.urls
