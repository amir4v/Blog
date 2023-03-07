from rest_framework import serializers

from accounts.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=256, source='user.email')
    
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'birth_date', 'location', 'status', 'avatar', 'user']
        read_only_fields = ['user']
    
    def validate(self, attrs):
        avatar = attrs.get('avatar')
        return super().validate(attrs)
