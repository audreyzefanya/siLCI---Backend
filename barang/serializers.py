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
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = PerusahaanImpor
        fields = ['id', 'nama', 'deskripsi', 'logo', 'logo_url']

    def get_logo_url(self, perusahaan):
        if perusahaan.logo:
            return self.context['request'].build_absolute_uri(perusahaan.logo.url)
        return None