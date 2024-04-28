from collections import namedtuple
from django.db import connection
from django.db import IntegrityError
from django.http import JsonResponse
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
    
    def rejectPengadaan(self, request, pengadaan_id):
        try:
            pengadaan = PengadaanBarangImpor.objects.get(pk=pengadaan_id)
        except PengadaanBarangImpor.DoesNotExist:
            return Response({"error": "Pengadaan Impor tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        pengadaan.status = 0

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

class DashboardViewSet(viewsets.ViewSet):
    def namedtuplefetchall(cursor):
        desc = cursor.description
        result = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
        return result

    def getDataDashboardStafPengadaan(self, request):
        cursor = connection.cursor()

        # Ambil jumlah pengadaan seluruhnya
        cursor.execute("SELECT COUNT(*) AS jumlah FROM barang_pengadaanbarangimpor")
        jumlah_pengadaan = DashboardViewSet.namedtuplefetchall(cursor)

        # Ambil jumlah pengadaan yang aktif saja
        cursor.execute("SELECT COUNT(*) AS jumlah FROM barang_pengadaanbarangimpor WHERE STATUS > 0 AND STATUS <6")
        jumlah_pengadaan_aktif = DashboardViewSet.namedtuplefetchall(cursor)

        # Ambil jumlah pengadaan yang membutuhkan pembayaran
        cursor.execute("SELECT COUNT(*) AS jumlah FROM barang_pengadaanbarangimpor WHERE STATUS = 2")
        jumlah_pengadaan_payment = DashboardViewSet.namedtuplefetchall(cursor)

        # Ambil jumlah pengadaan by tanggal permintaan
        cursor.execute('SELECT "tanggalPermintaaan", COUNT(*) AS jumlah FROM barang_pengadaanbarangimpor GROUP BY "tanggalPermintaaan"')
        jumlah_pengadaan_by_tanggalpermintaan = DashboardViewSet.namedtuplefetchall(cursor)

        response_data = {
            'jumlah_pengadaan': jumlah_pengadaan[0]['jumlah'],
            'jumlah_pengadaan_aktif': jumlah_pengadaan_aktif[0]['jumlah'],
            'jumlah_pengadaan_payment': jumlah_pengadaan_payment[0]['jumlah'],
            'jumlah_pengadaan_by_date': jumlah_pengadaan_by_tanggalpermintaan,
        }
        return Response(response_data)
    
    def getDataDashboardAdminImpor(self, request):
        cursor = connection.cursor()
        email = request.data.get('email')

        try:
            admin = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Akun dengan email tersebut tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            perusahaan = PerusahaanImpor.objects.get(admin=admin)
        except:
            return Response({"error": "Perusahaan Impor tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        # Ambil jumlah barang
        cursor.execute(f'SELECT COUNT(*) AS jumlah FROM "barang_perusahaanimpor_listBarang" WHERE perusahaanimpor_id = {perusahaan.id}')
        jumlah_barang = DashboardViewSet.namedtuplefetchall(cursor)

        # Ambil jumlah seluruh pengadaan 
        cursor.execute(f"SELECT COUNT(*) AS jumlah FROM barang_pengadaanbarangimpor WHERE perusahaan_id = {perusahaan.id}")
        jumlah_pengadaan = DashboardViewSet.namedtuplefetchall(cursor)

        # Ambil jumlah pengadaan yang aktif saja
        cursor.execute(f"SELECT COUNT(*) AS jumlah FROM barang_pengadaanbarangimpor WHERE STATUS > 0 AND STATUS <6 AND perusahaan_id = {perusahaan.id}")
        jumlah_pengadaan_aktif = DashboardViewSet.namedtuplefetchall(cursor)

        # Ambil jumlah pengadaan yang membutuhkan pembayaran
        cursor.execute(f"SELECT COUNT(*) AS jumlah FROM barang_pengadaanbarangimpor WHERE STATUS = 1 AND perusahaan_id = {perusahaan.id}")
        jumlah_pengadaan_requested = DashboardViewSet.namedtuplefetchall(cursor)

        # Ambil jumlah pengadaan by tanggal permintaan
        cursor.execute(f'SELECT "tanggalPermintaaan", COUNT(*) AS jumlah FROM barang_pengadaanbarangimpor WHERE perusahaan_id = {perusahaan.id} GROUP BY "tanggalPermintaaan"')
        jumlah_pengadaan_by_tanggalpermintaan = DashboardViewSet.namedtuplefetchall(cursor)

        response_data = {
            'jumlah_barang': jumlah_barang[0]['jumlah'],
            'jumlah_pengadaan': jumlah_pengadaan[0]['jumlah'],
            'jumlah_pengadaan_aktif': jumlah_pengadaan_aktif[0]['jumlah'],
            'jumlah_pengadaan_requested': jumlah_pengadaan_requested[0]['jumlah'],
            'jumlah_pengadaan_by_date': jumlah_pengadaan_by_tanggalpermintaan,
        }

        return Response(response_data)

        
        
