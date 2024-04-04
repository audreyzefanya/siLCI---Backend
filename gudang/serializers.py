from rest_framework import serializers
from .models import Gudang, BarangGudang
from barang.models import Barang
from pabrik.models import PermintaanPengiriman

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

class PermintaanPengirimanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermintaanPengiriman
        fields = '__all__'

class PermintaanPengirimanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermintaanPengiriman
        fields = ['status']
        read_only_fields = ['kode_permintaan', 'pabrik', 'gudang', 'barang', 'jumlah', 'waktu_permintaan', 'tanggal_pengiriman']