from rest_framework import viewsets, status
from rest_framework.response import Response

from barang.serializers import BarangSerializer
from .models import Barang

class BarangViewSet(viewsets.ViewSet):
    def getAllBarang(self, request):
        barangs = Barang.objects.all()
        serializer = BarangSerializer(barangs, many=True)
        return Response(serializer.data)

    def createBarang(self, request):
        serializer = BarangSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)