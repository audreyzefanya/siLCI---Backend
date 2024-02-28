from rest_framework import serializers
from .models import *

class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = '__all__'