from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import *
from .serializers import *


class PabrikViewSet(viewsets.ViewSet):
    def getAllPabrik(self, request):
        pabriks = Pabrik.objects.all()
        serializer = PabrikSerializer(pabriks, many=True)
        return Response(serializer.data)

    def getPabrik(self, request, pabrik_name):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        pabrik_serializer = PabrikSerializer(pabrik)
        daftarBarang = BarangPabrik.objects.filter(pabrik=pabrik)
        barang_serializer = BarangPabrikSerializer(daftarBarang, many=True)
        
        data = {
            "id": pabrik_serializer.data['id'],
            "nama": pabrik_serializer.data['nama'],
            "alamat": pabrik_serializer.data['alamat'],
            "listBarang": barang_serializer.data
        }
        
        return Response(data)
    
    def getAllBarangPabrik(self, request):
        barangpabriks = BarangPabrik.objects.all()
        serializer = BarangPabrikSerializer(barangpabriks, many=True)
        return Response(serializer.data)

    def createPabrik(self, request):
        serializer = PabrikSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def detailPabrik(self, request, pabrik_id):
#         try:
#             pabrik = Pabrik.objects.get(pk=pabrik_id)
#             serializer = PabrikSerializer(pabrik)
#             return Response(serializer.data)
#         except Pabrik.DoesNotExist:
#             return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
#
#     def updatePabrik(self, request, pabrik_id):
#         try:
#             pabrik = Pabrik.objects.get(pk=pabrik_id)
#         except Pabrik.DoesNotExist:
#             return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = PabrikSerializer(pabrik, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#

class BarangPabrikViewSet(viewsets.ViewSet):
    def addBarangToPabrik(self, request, pabrik_name):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        barang_id = request.data.get('id')
        if not barang_id:
            return Response({"error": "Tidak menemukan id pada request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            barang = Barang.objects.get(pk=barang_id)
        except Barang.DoesNotExist:
            return Response({"error": f"Barang dengan ID {barang_id} tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        try:
            barangpabrik = BarangPabrik.objects.get(barang=barang_id, pabrik=pabrik.id)
            return Response({"message": "Barang sudah ada pada pabrik tersebut"}, status=status.HTTP_400_BAD_REQUEST)
        except BarangPabrik.DoesNotExist:
            pass

        new_barang_pabrik = BarangPabrik.objects.create(barang=barang, pabrik=pabrik)
        return Response({"message": f"Barang {barang.nama} telah ditambahkan pada {pabrik.nama}"}, status=status.HTTP_200_OK)

    def getBarangInPabrik(self, request, pabrik_name):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        daftarBarang = BarangPabrik.objects.filter(pabrik=pabrik.id)
        serializers = BarangPabrikSerializer(daftarBarang, many=True)
        return Response(serializers.data)

