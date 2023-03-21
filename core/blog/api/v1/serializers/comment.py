from rest_framework import serializers

from blog.models import Comment


class CommentModelSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(min_length=1, max_length=1000)
    
    class Meta:
        model = Comment
        fields = ['profile', 'post', 'comment']
    
    def validate(self, attrs):
        user = self.context.get('request').user
        user_profile = user.profile
        profile = attrs.get('profile')
        
        if not user.is_superuser and user_profile != profile:
            """
            The given profile for this comment must be the same as
            the current user profile to prevent it from a user create a comment
            for other users.
            """
            raise serializers.ValidationError('Access denied.')
        
        return super().validate(attrs)
