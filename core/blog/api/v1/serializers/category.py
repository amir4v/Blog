from rest_framework import serializers

from blog.models import *
from core.utils import RangeLengthValidator


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
