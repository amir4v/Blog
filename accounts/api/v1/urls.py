from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'api-v1'

urlpatterns = [
    path('jwt/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # login
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('user/activation/<str:token>/', views.UserActivationAPIView.as_view(), name='user-activation'),
    # path('user/activation-confirm/', views.UserActivationConfirmGenericAPIView.as_view(), name='user-activation-confirm'),
    
    path('user/forgot-password/', views.ForgotPasswordAPIView.as_view(), name='user-forgot-password'),
    path('user/forgot-password-confirm/', views.ForgotPasswordConfirmGenericAPIView.as_view(), name='user-forgot-password-confirm'),
    path('user/forgot-password-verify/<str:token>/', views.ForgotPasswordVerifyAPIView.as_view(), name='user-forgot-password-verify'),
    
    path('user/reset-email/', views.ResetEmailGenericAPIView.as_view(), name='user-reset-email'),
    path('user/reset-email-verify/<str:token>/', views.ResetEmailVerifyAPIView.as_view(), name='user-reset-email-verify'),
]

router = DefaultRouter()

router.register('user', views.UserModelViewSet, basename='user')
"""
user/
    pre-register/
    register/
    me/
    profile/
    reset-password/
    reset-username/
    # /login/
    # login/
    logout/
"""

router.register('profile', views.ProfileModelViewSet, basename='profile')

urlpatterns += router.urls
