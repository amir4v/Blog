from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.v1.serializers import *


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
