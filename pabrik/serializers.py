from django.contrib.auth.models import User, Group
from rest_framework import serializers
from barang.serializers import BarangSerializer
from .models import *

class PabrikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pabrik
        fields = '__all__'

class BarangPabrikSerializer(serializers.ModelSerializer):
    barang = BarangSerializer()

    class Meta:
        model = BarangPabrik
        fields = ['barang', 'stok']

class BatchProduksiSerializer(serializers.ModelSerializer):
    barang = BarangSerializer()
    pabrik = PabrikSerializer()

    class Meta:
        model = BatchProduksi
        fields = '__all__'

    def create(self, validated_data):
        barang = self.context['barang']
        pabrik = self.context['pabrik']
        validated_data['barang'] = barang
        validated_data['pabrik'] = pabrik
        return super().create(validated_data)

class PermintaanPengirimanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermintaanPengiriman
        fields = '__all__'

class PermintaanPengirimanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermintaanPengiriman
        fields = ['status']
        read_only_fields = ['kode_permintaan', 'pabrik', 'gudang', 'barang', 'jumlah', 'waktu_permintaan', 'tanggal_pengiriman']