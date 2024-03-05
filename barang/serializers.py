from rest_framework import serializers
from .models import *

class MerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merk
        fields = ('id', 'nama')

class BarangSerializer(serializers.ModelSerializer):
    merk = MerkSerializer()
    
    class Meta:
        model = Barang
        fields = '__all__'

class PerusahaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerusahaanImpor
        fields = '__all__'