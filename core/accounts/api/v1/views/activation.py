from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class UserActivationAPIView(APIView):
    def get(self, request, token):
        pass


class UserActivationConfirmAPIView(APIView):
    def post(self, request):
        pass
