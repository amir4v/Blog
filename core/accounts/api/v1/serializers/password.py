from rest_framework import serializers


class ForgotPasswordConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
