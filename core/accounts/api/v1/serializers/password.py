from rest_framework import serializers


class ForgotPasswordConfirmEmailSerializer(serializers.Serializer):
    """
    Here we are not validating for email being exist because in the view
    we need user object so we did the existing validation in the view.
    """
    
    email = serializers.EmailField()
