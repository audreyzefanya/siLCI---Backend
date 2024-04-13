from django.db import models
import uuid

class JenisGudang(models.Model):
    nama = models.CharField(max_length=255, unique=True)

class Gudang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255)
    kapasitas = models.BigIntegerField()
    jenis = models.ForeignKey(JenisGudang, on_delete=models.CASCADE)

class BarangGudang(models.Model):
    barang = models.ForeignKey('barang.Barang', on_delete=models.CASCADE, default=uuid.uuid4, primary_key=True, related_name='barang_gudang')
    gudang = models.ForeignKey('Gudang', on_delete=models.CASCADE, default=uuid.uuid4, related_name='gudang')
    stok = models.IntegerField(default = 0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['barang', 'gudang'], name='unique_barang_gudang'
            )
        ]
