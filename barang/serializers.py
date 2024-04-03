from rest_framework import serializers
from .models import *

class MerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merk
        fields = ('id', 'nama')

class BarangSerializer(serializers.ModelSerializer):
    merk = MerkSerializer(read_only=True)
    merk_id = serializers.PrimaryKeyRelatedField(
        queryset=Merk.objects.all(), write_only=True, source='merk'
    )

    class Meta:
        model = Barang
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PerusahaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerusahaanImpor
        fields = ['id', 'nama', 'deskripsi', 'logo', 'admin']

class PengadaanSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return dict(PengadaanBarangImpor.STATUS_PENGADAAN).get(obj.status)
    
    class Meta:
        model = PengadaanBarangImpor
        fields = '__all__'