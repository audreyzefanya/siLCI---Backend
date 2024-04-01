from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import *
from .serializers import *
import cloudinary.uploader

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
    
    def detailBarang(self, request, barang_id):
        try:
            barang = Barang.objects.get(pk=barang_id)
            serializer = BarangSerializer(barang)
            return Response(serializer.data)
        except Barang.DoesNotExist:
            return Response({"error": "Barang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
    def updateBarang(self, request, barang_id):
        try:
            barang = Barang.objects.get(pk=barang_id)
        except Barang.DoesNotExist:
            return Response({"error": "Barang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BarangSerializer(barang, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PerusahaanViewSet(viewsets.ViewSet):
    def getAllPerusahaan(self, request):
        perusahaan = PerusahaanImpor.objects.all().order_by('id')
        serializer = PerusahaanSerializer(perusahaan, many=True, context={'request': request})
        return Response(serializer.data)
    
    def getPerusahaan(self, request, perusahaan_id):
        try:
            perusahaan = PerusahaanImpor.objects.get(pk=perusahaan_id)
        except PerusahaanImpor.DoesNotExist:
            return Response({"error": "Perusahaan tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PerusahaanSerializer(perusahaan, context={'request': request})
        return Response(serializer.data)

    def createPerusahaan(self, request):
        logo = cloudinary.uploader.upload(request.data["logo"],
                                folder = "perusahaanlogo/",
                                public_id=request.data["nama"])
    
        request.data["logo"] = logo["url"]
        serializer = PerusahaanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def addBarangToPerusahaan(self, request, perusahaan_id):
        try:
            perusahaan = PerusahaanImpor.objects.get(pk=perusahaan_id)
        except PerusahaanImpor.DoesNotExist:
            return Response({"error": "Perusahaan tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        barang_id = request.data.get('id') # Cek apakah field request udah benar
        if not barang_id:
            return Response({"error": "Tidak menemukan id pada request"}, status=status.HTTP_400_BAD_REQUEST)

        if perusahaan.listBarang.filter(id=barang_id).exists(): # Cek apakah barang sudah ada pada perusahaan tersebut
            return Response({"message": f"Barang tersebut telah didaftarkan pada perusahaan tersebut"}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            barang = Barang.objects.get(pk=barang_id)
        except Barang.DoesNotExist: # Cek apakah ID nya benar
            return Response({"error": "Barang dengan ID tersebut tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        perusahaan.listBarang.add(barang)
        return Response({"message": f"Barang {barang.nama} telah ditambahkan pada Perusahaan {perusahaan.nama}"}, status=status.HTTP_200_OK)
    
    def getBarangPerusahaan(self, request, perusahaan_id):
        try:
            perusahaan = PerusahaanImpor.objects.get(pk=perusahaan_id)
        except PerusahaanImpor.DoesNotExist:
            return Response({"error": "Perusahaan tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        barangs = perusahaan.listBarang.all()
        serializer = BarangSerializer(barangs, many=True)
        return Response(serializer.data)
