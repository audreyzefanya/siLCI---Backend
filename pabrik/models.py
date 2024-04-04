from django.db import models
from barang.models import Barang
from gudang.models import Gudang
import uuid

class Pabrik(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=50, unique=True)
    alamat = models.CharField(max_length=200)

class BarangPabrik(models.Model):
    barang = models.ForeignKey('barang.Barang', on_delete=models.CASCADE, default=uuid.uuid4, primary_key=True, related_name='barang_pabrik')
    pabrik = models.ForeignKey('Pabrik', on_delete=models.CASCADE, default=uuid.uuid4, related_name='pabrik')
    stok = models.IntegerField(default = 0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['barang', 'pabrik'], name='unique_barang_pabrik'
            )
        ]

class BatchProduksi(models.Model):
    kode_produksi = models.CharField(max_length=10, primary_key=True)
    barang = models.ForeignKey('barang.Barang', on_delete=models.CASCADE, default=uuid.uuid4, related_name='barang_batch')
    pabrik = models.ForeignKey('Pabrik', on_delete=models.CASCADE, default=uuid.uuid4, related_name='pabrik_batch')
    jumlah = models.IntegerField(default=0)
    tanggal_produksi = models.DateField()
    status = models.IntegerField(default=1)

class PermintaanPengiriman(models.Model):
    kode_permintaan = models.CharField(max_length=10, primary_key=True)
    pabrik = models.ForeignKey(Pabrik, on_delete=models.CASCADE)
    gudang = models.ForeignKey(Gudang, on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    status = models.IntegerField()
    waktu_permintaan = models.DateTimeField(auto_now_add=True)
    tanggal_pengiriman = models.DateField(null=True, blank=True)
