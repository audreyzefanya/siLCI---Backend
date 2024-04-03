from rest_framework import serializers
from .models import Gudang, BarangGudang
from barang.models import Barang

class GudangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gudang
        fields = '__all__'

class BarangGudangSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarangGudang
        fields = '__all__'

class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = '__all__'