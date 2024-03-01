from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class PabrikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pabrik
        fields = '__all__'

class BarangPabrikSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarangPabrik
        fields = '__all__'