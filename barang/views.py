from django.db import IntegrityError
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

class PengadaanViewSet(viewsets.ViewSet):
    def addPengadaaanImpor(self, request):
        serializer = PengadaanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def increaseStatusPengadaan(self, request, pengadaan_id):
        try:
            pengadaan = PengadaanBarangImpor.objects.get(pk=pengadaan_id)
        except PengadaanBarangImpor.DoesNotExist:
            return Response({"error": "Pengadaan Impor tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        pengadaan.status = pengadaan.status + 1

        try:
            pengadaan.save()  
        except IntegrityError:
            return Response({"error": "Gagal menyimpan perubahan status"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": f"Status pengadaan dengan id {pengadaan.id} berhasil diubah menjadi {pengadaan.status}"}, status=status.HTTP_200_OK)
    
    def detailPengadaan(self, request, pengadaan_id=None):
        try:
            pengadaan = PengadaanBarangImpor.objects.get(pk=pengadaan_id)
        except PengadaanBarangImpor.DoesNotExist:
            return Response({"error": "Pengadaan Impor tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PengadaanSerializer(pengadaan)
        return Response(serializer.data)
    
    def getAllPengadaan(self, request):
        pengadaan = PengadaanBarangImpor.objects.all()
        serializer = PengadaanSerializer(pengadaan, many=True)
        return Response(serializer.data)
    
    def uploadInvoiceFile(self, request, pengadaan_id=None):
        try:
            pengadaan = PengadaanBarangImpor.objects.get(pk=pengadaan_id)
        except PengadaanBarangImpor.DoesNotExist:
            return Response({"error": "Pengadaan Impor tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        if 'fileInvoice' in request.FILES:
            file_invoice = request.FILES['fileInvoice']
            upload_response = cloudinary.uploader.upload(file_invoice,
                                                        folder="pengadaanInvoice/",
                                                        public_id=f"invoice_{pengadaan_id}")
            
            pengadaan.fileInvoice = upload_response['url']
            pengadaan.save()
            return Response({"message": "Invoice file uploaded successfully", "fileUrl": upload_response['url']}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No invoice file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
    def uploadPaymentFile(self, request, pengadaan_id=None):
        try:
            pengadaan = PengadaanBarangImpor.objects.get(pk=pengadaan_id)
        except PengadaanBarangImpor.DoesNotExist:
            return Response({"error": "Pengadaan Impor tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        if 'filePayment' in request.FILES:
            file_payment = request.FILES['filePayment']
            upload_response = cloudinary.uploader.upload(file_payment,
                                                        folder="pengadaanPayment/",
                                                        public_id=f"payment_{pengadaan_id}")
            
            pengadaan.filePayment = upload_response['url']
            pengadaan.save()
            return Response({"message": "Payment file uploaded successfully", "fileUrl": upload_response['url']}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No payment file provided"}, status=status.HTTP_400_BAD_REQUEST)

