from rest_framework import serializers

from .models import *


class MerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merk
        fields = ('id', 'nama')

class BarangSerializer(serializers.ModelSerializer):
    merk = serializers.PrimaryKeyRelatedField(queryset=Merk.objects.all())
    
    class Meta:
        model = Barang
        fields = '__all__'
    
class PerusahaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerusahaanImpor
        fields = '__all__'