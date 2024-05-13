from django.db import connection
from django.db.models import Max
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

from barang.models import Barang
from pabrik.models import PermintaanPengiriman
from pabrik.serializers import PermintaanPengirimanSerializer

from .models import *
from .serializers import *


class GudangViewSet(viewsets.ViewSet):
    def listGudang(self, request):
        gudang = Gudang.objects.all()
        serializer = GudangSerializer(gudang, many=True)
        return Response(serializer.data)

    def createGudang(self, request):
        nama_gudang = request.data.get('nama')
        if Gudang.objects.filter(nama=nama_gudang).exists():
            return Response({"error": "Nama gudang sudah ada."}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"message": "Barang sudah ada pada gudang tersebut"}, status=status.HTTP_400_BAD_REQUEST)
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

    def detailGudang(self, request, gudang_id):
        try:
            gudang = Gudang.objects.get(pk=gudang_id)
        except Gudang.DoesNotExist:
            return Response({"error": "Gudang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        barang_gudang = BarangGudang.objects.filter(gudang=gudang)
        data = []

        for bg in barang_gudang:
            nama_barang = bg.barang.nama
            data.append({
                "id_barang": bg.barang.id,
                "nama_barang": nama_barang,
                "stok": bg.stok
            })

        response_data = {
            "id_gudang": gudang_id,
            "nama_gudang": gudang.nama,
            "alamat_gudang": gudang.alamat,
            "kapasitas_gudang": gudang.kapasitas,
            "jenis_gudang": gudang.jenis.nama,
            "barang": data
        }

        return Response(response_data)

    def updateDetailGudang(self, request, gudang_id):
        try:
            gudang = Gudang.objects.get(pk=gudang_id)
        except Gudang.DoesNotExist:
            return Response({"error": "Gudang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GudangSerializer(gudang, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def addStokGudang(self, request):
        try:
            barang_id = request.data.get('barang')
            gudang_id = request.data.get('gudang')

            baranggudang = BarangGudang.objects.get(barang=barang_id, gudang=gudang_id)
            newStok = baranggudang.stok + request.data.get('stok')

            cursor = connection.cursor()
    
            try:
                cursor.execute("UPDATE gudang_baranggudang SET stok = %s WHERE barang_id = %s AND gudang_id = %s", [newStok, barang_id, gudang_id])
            except:
                return Response({"error": f"Error menambahkan stok barang {baranggudang.stok}"}, status=status.HTTP_404_NOT_FOUND)
        except BarangGudang.DoesNotExist:
            try:
                barang = Barang.objects.get(pk=request.data.get('barang'))
            except Barang.DoesNotExist:
                return Response({"error": f"Barang dengan ID tersebut tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                gudang = Gudang.objects.get(pk=request.data.get('gudang'))
            except Gudang.DoesNotExist:
                return Response({"error": "Gudang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
            
            baranggudang = BarangGudang.objects.create(barang=barang, gudang=gudang, stok=request.data.get('stok'))
            pass

        return Response({"message": f"Stok barang {baranggudang.barang.nama} telah ditambahkan pada {baranggudang.gudang.nama}"}, status=status.HTTP_200_OK)
    
    def addStokGudang(self, request):
        try:
            barang_id = request.data.get('barang')
            gudang_id = request.data.get('gudang')

            baranggudang = BarangGudang.objects.get(barang=barang_id, gudang=gudang_id)
            newStok = baranggudang.stok + request.data.get('stok')

            cursor = connection.cursor()
    
            try:
                cursor.execute("UPDATE gudang_baranggudang SET stok = %s WHERE barang_id = %s AND gudang_id = %s", [newStok, barang_id, gudang_id])
            except:
                return Response({"error": f"Error menambahkan stok barang {baranggudang.stok}"}, status=status.HTTP_404_NOT_FOUND)
        except BarangGudang.DoesNotExist:
            try:
                barang = Barang.objects.get(pk=request.data.get('barang'))
            except Barang.DoesNotExist:
                return Response({"error": f"Barang dengan ID tersebut tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                gudang = Gudang.objects.get(pk=request.data.get('gudang'))
            except Gudang.DoesNotExist:
                return Response({"error": "Gudang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
            
            baranggudang = BarangGudang.objects.create(barang=barang, gudang=gudang, stok=request.data.get('stok'))
            pass

        return Response({"message": f"Stok barang {baranggudang.barang.nama} telah ditambahkan pada {baranggudang.gudang.nama}"}, status=status.HTTP_200_OK)

    def reduceStokGudang(self, request):
        try:
            barang_id = request.data.get('barang')
            gudang_id = request.data.get('gudang')

            # Retrieve the current stock
            baranggudang = BarangGudang.objects.get(barang=barang_id, gudang=gudang_id)
            currentStok = baranggudang.stok
            reduceStok = int(request.data.get('stok', 0))  # Default to 0 if not provided

            if reduceStok > currentStok:
                return Response({"error": "Stok yang diminta lebih besar daripada stok yang tersedia"}, status=status.HTTP_400_BAD_REQUEST)

            newStok = currentStok - reduceStok

            # Update the stock using the database cursor
            cursor = connection.cursor()
            try:
                cursor.execute("UPDATE gudang_baranggudang SET stok = %s WHERE barang_id = %s AND gudang_id = %s", [newStok, barang_id, gudang_id])
            except Exception as e:
                return Response({"error": f"Error mengurangi stok barang: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)
        except BarangGudang.DoesNotExist:
            return Response({"error": "Barang atau gudang tidak ditemukan dalam gudang"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": f"Stok barang {baranggudang.barang.nama} telah dikurangi pada {baranggudang.gudang.nama}"}, status=status.HTTP_200_OK)

class PermintaanPengirimanViewSet(viewsets.ViewSet):
    def getDaftarPengirimanGudang(self, request, gudang_id):
        try:
            gudang = Gudang.objects.get(pk=gudang_id)
        except Gudang.DoesNotExist:
            return Response({"error": "Gudang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        permintaan_pengiriman = PermintaanPengiriman.objects.filter(gudang=gudang)
        data = []
        for pengiriman in permintaan_pengiriman:
            data.append({
                "kode_permintaan": pengiriman.kode_permintaan,
                "pabrik": pengiriman.pabrik.nama,
                "gudang": pengiriman.gudang.nama,
                "barang": pengiriman.barang.nama,
                "jumlah": pengiriman.jumlah,
                "status": pengiriman.status,
                "waktu_permintaan": pengiriman.waktu_permintaan,
                "tanggal_pengiriman": pengiriman.tanggal_pengiriman
            })
        return Response(data)
    
    def addPermintaanPengiriman(self, request, gudang_id):
        try:
            gudang = Gudang.objects.get(pk=gudang_id)
        except Gudang.DoesNotExist:
            return Response({"error": "Gudang tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        last_permintaan = PermintaanPengiriman.objects.aggregate(Max('kode_permintaan'))
        last_code = last_permintaan['kode_permintaan__max']
        if last_code:
            next_code = int(last_code[3:]) + 1 
        else:
            next_code = 1
        new_kode_permintaan = f"REQ{next_code:03}"
        
        request.data['kode_permintaan'] = new_kode_permintaan
        request.data['gudang'] = gudang.id  

        if 'barang_id' in request.data and 'gudang_id' in request.data:
            request.data['barang'] = request.data.pop('barang_id')
            request.data['gudang'] = request.data.pop('gudang_id')

        serializer = PermintaanPengirimanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def updateStatusGudang(self, request, kode_permintaan):
        try:
            permintaan = PermintaanPengiriman.objects.get(kode_permintaan=kode_permintaan)
        except PermintaanPengiriman.DoesNotExist:
            return Response({"error": "Kode pengiriman tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        # Mengubah request data untuk memanggil metode addStokGudang dengan mengganti "stok" menjadi "jumlah"
        request.data['stok'] = request.data['jumlah']

        if permintaan.status != 4 and request.data.get('status') == 4:
            try:
                BarangGudangViewSet().addStokGudang(request)
            except Exception as e:
                return Response({"error": f"Error menambahkan stok barang: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermintaanPengirimanSerializer(permintaan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
