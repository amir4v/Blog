from django.core import validators

from rest_framework import serializers

from blog.models import Post
from core.utils import upload_banner


class PostModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, max_length=128)
    content = serializers.CharField(min_length=1)
    
    banner_image = serializers.ImageField(write_only=True, required=False,
                        validators=[
                            validators.FileExtensionValidator(
                                allowed_extensions=['jpeg', 'jpg', 'png']
                            )
                        ]
                   )
    banner = serializers.CharField(max_length=256, read_only=True)
    """
    We upload the banner image file to a temporary field called banner_image
    and then upload the file and get the path to the banner field.
    """
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'profile',
                  'category', 'banner_image', 'banner']
        read_only_fields = ['id', 'banner']
    
    def validate(self, attrs):
        user = self.context.get('request').user
        user_profile = user.profile
        profile = attrs.get('profile')
        banner = attrs.get('banner_image', None)
        category = attrs.get('category')
        
        if not user.is_superuser and user_profile != profile:
            """
            The given profile for this post must be the same as
            the current user profile to prevent it from a user create a post
            for other users.
            """
            raise serializers.ValidationError('Access denied.')
        
        if banner:
            """
            If user upload a banner_image, we upload the file and get
            the path to the banner field and then pop the banner_image
            because it's not in the user model fields.
            """
            path = upload_banner(banner)
            attrs['banner'] = path
        attrs.pop('banner_image', None)
        
        if not (
            user.is_superuser or user_profile.categories.filter(pk=category.pk).exists()
        ):
            """
            The given category for this post must be one of
            current user categories to prevent it from a user create a post
            for other users categories.
            """
            raise serializers.ValidationError('Access denied.')
        
        return super().validate(attrs)
