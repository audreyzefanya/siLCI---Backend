from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import *
from .serializers import *


class PabrikViewSet(viewsets.ViewSet):
    def getAllPabrik(self, request):
        pabriks = Pabrik.objects.all()
        serializer = PabrikSerializer(pabriks, many=True)
        return Response(serializer.data)

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
# class PerusahaanViewSet(viewsets.ViewSet):
#     def getAllPerusahaan(self, request):
#         perusahaan = PerusahaanImpor.objects.all()
#         serializer = PerusahaanSerializer(perusahaan, many=True)
#         return Response(serializer.data)
#
#     def createPerusahaan(self, request):
#         serializer = PerusahaanSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def addPabrikToPerusahaan(self, request, perusahaan_id):
#         try:
#             perusahaan = PerusahaanImpor.objects.get(pk=perusahaan_id)
#         except PerusahaanImpor.DoesNotExist:
#             return Response({"error": "Perusahaan tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
#
#         pabrik_id = request.data.get('id') # Cek apakah field request udah benar
#         if not pabrik_id:
#             return Response({"error": "Tidak menemukan id pada request"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if perusahaan.listPabrik.filter(id=pabrik_id).exists(): # Cek apakah pabrik sudah ada pada perusahaan tersebut
#             return Response({"message": f"Pabrik tersebut telah didaftarkan pada perusahaan tersebut"}, status=status.HTTP_200_OK)
#
#         try:
#             pabrik = Pabrik.objects.get(pk=pabrik_id)
#         except Pabrik.DoesNotExist: # Cek apakah ID nya benar
#             return Response({"error": "Pabrik dengan ID tersebut tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
#
#         perusahaan.listPabrik.add(pabrik)
#         return Response({"message": f"Pabrik {pabrik.nama} telah ditambahkan pada Perusahaan {perusahaan.nama}"}, status=status.HTTP_200_OK)
#
#     def getPabrikPerusahaan(self, request, perusahaan_id):
#         try:
#             perusahaan = PerusahaanImpor.objects.get(pk=perusahaan_id)
#         except PerusahaanImpor.DoesNotExist:
#             return Response({"error": "Perusahaan tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
#
#         pabriks = perusahaan.listPabrik.all()
#         serializer = PabrikSerializer(pabriks, many=True)
#         return Response(serializer.data)
