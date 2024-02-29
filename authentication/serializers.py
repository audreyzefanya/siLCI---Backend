from django.contrib.auth.models import User, Group
from rest_framework import serializers
from authentication.models import CustomUser



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "email", "role"
        ]



