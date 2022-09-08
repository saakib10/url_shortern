from rest_framework import serializers
from .models import Shortener


class UrltSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shortener
        fields = '__all__'