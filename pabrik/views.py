from django.db.models import Max
from django.db import connection
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

    def updatePabrik(self, request, pabrik_name):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PabrikSerializer(pabrik, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
            BarangPabrik.objects.get(barang=barang_id, pabrik=pabrik.id)
            return Response({"message": "Barang sudah ada pada pabrik tersebut"}, status=status.HTTP_400_BAD_REQUEST)
        except BarangPabrik.DoesNotExist:
            pass

        BarangPabrik.objects.create(barang=barang, pabrik=pabrik)
        return Response({"message": f"Barang {barang.nama} telah ditambahkan pada {pabrik.nama}"}, status=status.HTTP_200_OK)

    def getBarangInPabrik(self, request, pabrik_name):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        daftarBarang = BarangPabrik.objects.filter(pabrik=pabrik.id)
        serializers = BarangPabrikSerializer(daftarBarang, many=True)
        return Response(serializers.data)

    def updateStokBarangInPabrik(self, batch_produksi, pabrik_name, barang_id):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        try:
            barang = Barang.objects.get(pk=barang_id)
        except Barang.DoesNotExist:
            return Response({"error": f"Barang dengan ID {barang_id} tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        try:
            barangpabrik = BarangPabrik.objects.get(barang=barang, pabrik=pabrik)
            newStok = barangpabrik.stok + batch_produksi.jumlah
            cursor = connection.cursor()

            try:
                cursor.execute("UPDATE pabrik_barangpabrik SET stok = %s WHERE barang_id = %s AND pabrik_id = %s", [newStok, barang_id, pabrik.id])
            except:
                return Response({"error": f"Error mengupdate stok barang {barangpabrik.stok}"}, status=status.HTTP_404_NOT_FOUND)

        except BarangPabrik.DoesNotExist:
            barangpabrik = BarangPabrik.objects.create(barang=barang, pabrik=pabrik, stok=batch_produksi.jumlah)

        return Response({"message": f"Stok barang {barangpabrik.barang.nama} telah diperbarui pada {barangpabrik.pabrik.nama}"}, status=status.HTTP_200_OK)

    def reduceStokBarangInPabrik(self, permintaan, pabrik_name, barang_id):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        try:
            barang = Barang.objects.get(pk=barang_id)
        except Barang.DoesNotExist:
            return Response({"error": f"Barang dengan ID {barang_id} tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        try:
            barangpabrik = BarangPabrik.objects.get(barang=barang, pabrik=pabrik)
            currentStok = barangpabrik.stok
            reduceStok = permintaan.jumlah

            if reduceStok > currentStok:
                return Response({"error": "Stok yang diminta lebih besar daripada stok yang tersedia"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                newStok = currentStok - reduceStok

            cursor = connection.cursor()
            try:
                cursor.execute("UPDATE pabrik_barangpabrik SET stok = %s WHERE barang_id = %s AND pabrik_id = %s", [newStok, barang_id, pabrik.id])
            except:
                return Response({"error": f"Error mengupdate stok barang {barangpabrik.stok}"}, status=status.HTTP_404_NOT_FOUND)
        except BarangPabrik.DoesNotExist:
            return Response({"error": f"Barang {barang.nama} tidak ditemukan pada pabrik {pabrik.nama}"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": f"Stok barang {barangpabrik.barang.nama} telah diperbarui pada {barangpabrik.pabrik.nama}"}, status=status.HTTP_200_OK)


class PermintaanPengirimanViewSet(viewsets.ViewSet):
    def getAllPermintaanPengiriman(self, request):
        permintaan_pengiriman = PermintaanPengiriman.objects.all()
        serializer = PermintaanPengirimanSerializer(permintaan_pengiriman, many=True)
        return Response(serializer.data)

    def getDaftarPengiriman(self, request, pabrik_name):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        permintaan_pengiriman = PermintaanPengiriman.objects.filter(pabrik=pabrik)
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
    
    def addPermintaanPengiriman(self, request, pabrik_name):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        last_permintaan = PermintaanPengiriman.objects.aggregate(Max('kode_permintaan'))
        last_code = last_permintaan['kode_permintaan__max']
        if last_code:
            next_code = int(last_code[3:]) + 1 
        else:
            next_code = 1
        new_kode_permintaan = f"REQ{next_code:03}"
        
        request.data['kode_permintaan'] = new_kode_permintaan
        request.data['pabrik'] = pabrik.id  

        serializer = PermintaanPengirimanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def updateStatus(self, request, kode_permintaan):
        try:
            permintaan = PermintaanPengiriman.objects.get(kode_permintaan=kode_permintaan)
        except PermintaanPengiriman.DoesNotExist:
            return Response({"error": "Kode pengiriman tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        if permintaan.status != 4 and request.data.get('status') == 4:
            BarangPabrikViewSet().reduceStokBarangInPabrik(permintaan, permintaan.pabrik.nama, permintaan.barang.id)

        serializer = PermintaanPengirimanSerializer(permintaan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BatchProduksiViewSet(viewsets.ViewSet):
    def getAllBatchProduksiInPabrik(self, request, pabrik_name):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        daftarBatch = BatchProduksi.objects.filter(pabrik=pabrik.id)

        if not daftarBatch:
            return Response({"error": "Tidak ada batch produksi pada pabrik ini"}, status=status.HTTP_404_NOT_FOUND)

        serializers = BatchProduksiSerializer(daftarBatch, many=True)
        return Response(serializers.data)

    def getAllBatchProduksiStatus(self, request):
        daftarBatch = BatchProduksi.objects.all()
        serializers = BatchProduksiSerializer(daftarBatch, many=True)
        return Response(serializers.data)

    def getDetailBatchProduksiInPabrik(self, request, pabrik_name, batch_code):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        try:
            batch_produksi = BatchProduksi.objects.get(pabrik=pabrik, kode_produksi=batch_code)
        except BatchProduksi.DoesNotExist:
            return Response({"error": f"Batch Produksi dengan kode {batch_code} tidak ditemukan di pabrik {pabrik.nama}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BatchProduksiSerializer(batch_produksi)
        return Response(serializer.data)

    def addBatchProduksiToPabrik(self, request, pabrik_name):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        # Membuat kode batch produksi baru
        last_batchproduksi = BatchProduksi.objects.aggregate(Max('kode_produksi'))
        last_code = last_batchproduksi['kode_produksi__max']
        if last_code:
            next_code = int(last_code[2:]) + 1
        else:
            next_code = 1
        new_kode_produksi = f"BP{next_code:03}"
        request.data['kode_produksi'] = new_kode_produksi

        barang_id = request.data.get('barang_id')

        try:
            barang = Barang.objects.get(pk=barang_id)
        except Barang.DoesNotExist:
            return Response({"error": f"Barang dengan ID {barang_id} tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        new_batch_produksi = BatchProduksiSerializer(data=request.data, context={'barang': barang, 'pabrik': pabrik})
        new_batch_produksi.is_valid(raise_exception=True)
        new_batch_produksi.save()

        return Response({"message": f"Batch Produksi {new_kode_produksi} telah ditambahkan pada {pabrik.nama}"}, status=status.HTTP_200_OK)

    def updateBatchProduksiInPabrik(self, request, pabrik_name, batch_code):
        try:
            pabrik = Pabrik.objects.get(nama=pabrik_name)
        except Pabrik.DoesNotExist:
            return Response({"error": "Pabrik tidak dapat ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        try:
            batch_produksi = BatchProduksi.objects.get(kode_produksi=batch_code, pabrik=pabrik)
        except BatchProduksi.DoesNotExist:
            return Response({"error": f"Batch Produksi dengan kode {batch_code} tidak ditemukan di pabrik {pabrik.nama}"}, status=status.HTTP_404_NOT_FOUND)

        if batch_produksi.status < 4 and request.data.get('status') == 4:
            response = BarangPabrikViewSet().updateStokBarangInPabrik(batch_produksi, pabrik_name, batch_produksi.barang.id)
            if response.status_code != 200:
                return response

        updated_batch_produksi = BatchProduksiSerializer(instance=batch_produksi, data=request.data, partial=True, context={'pabrik': pabrik})
        updated_batch_produksi.is_valid(raise_exception=True)
        updated_batch_produksi.save()

        return Response({"message": f"Batch Produksi {batch_code} telah berhasil diperbarui"}, status=status.HTTP_200_OK)