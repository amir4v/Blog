from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.v1.serializers import CustomTokenObtainPairSerializer

from accounts.utils import IsNotAuthenticated


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView
    --------------------------
    (Actually) Login View
    ---------------------
    Takes username and password
    and returns an access token and a refresh token.
    """
    
    permission_classes = [IsNotAuthenticated]
    serializer_class = CustomTokenObtainPairSerializer
