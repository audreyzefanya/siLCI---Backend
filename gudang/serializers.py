from rest_framework import serializers
from .models import *

class GudangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gudang
        fields = '__all__'

class BarangGudangSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarangGudang
        fields = '__all__'