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