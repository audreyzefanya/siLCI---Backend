from rest_framework import viewsets, status
from rest_framework.response import Response
from barang.models import Barang
from .models import *
from .serializers import *

class GudangViewSet(viewsets.ViewSet):
    def listGudang(self, request):
        gudang = Gudang.objects.all()
        serializer = GudangSerializer(gudang, many=True)
        return Response(serializer.data)

    def createGudang(self, request):
        serializer = GudangSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BarangGudangViewSet(viewsets.ViewSet):
    def addBarangToGudang(self, request, gudang_id):
        try:
            gudang = Gudang.objects.get(pk=gudang_id)
        except Gudang.DoesNotExist:
            return Response({"error": "Gudang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        barang_id = request.data.get('id')
        if not barang_id:
            return Response({"error": "Tidak menemukan id pada request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            barang = Barang.objects.get(pk=barang_id)
        except Barang.DoesNotExist:
            return Response({"error": f"Barang dengan ID {barang_id} tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        try:
            baranggudang = BarangGudang.objects.get(barang=barang_id, gudang=gudang_id)
            return Response({"message": "Barang sudah ada pada gudang tersebut"}, status=status.HTTP_200_OK)
        except BarangGudang.DoesNotExist:
            pass

        new_barang_gudang = BarangGudang.objects.create(barang=barang, gudang=gudang)
        return Response({"message": f"Barang {barang.nama} telah ditambahkan pada {gudang.nama}"}, status=status.HTTP_200_OK)

    def listBarangPadaGudang(self, request, gudang_id):
        try:
            gudang = Gudang.objects.get(pk=gudang_id)
        except Gudang.DoesNotExist:
            return Response({"error": "Gudang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        barang_gudang = BarangGudang.objects.filter(gudang=gudang)
        serializer = BarangGudangSerializer(barang_gudang, many=True)

        return Response(serializer.data)