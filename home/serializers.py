from .models import *
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model= Blog
        exclude = ['created_at', 'updated_at']
    