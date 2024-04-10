from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Gudang, BarangGudang
from .serializers import GudangSerializer, BarangGudangSerializer
from pabrik.models import PermintaanPengiriman
from pabrik.serializers import PermintaanPengirimanSerializer
from barang.models import Barang

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
                "nama_barang": nama_barang,
                "stok": bg.stok
            })

        response_data = {
            "id_gudang": gudang_id,
            "nama_gudang": gudang.nama,
            "alamat_gudang": gudang.alamat,
            "kapasitas_gudang": gudang.kapasitas,
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

    def updateStatusGudang(self, request, kode_permintaan):
        try:
            permintaan = PermintaanPengiriman.objects.get(kode_permintaan=kode_permintaan)
        except PermintaanPengiriman.DoesNotExist:
            return Response({"error": "Kode pengiriman tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermintaanPengirimanSerializer(permintaan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
