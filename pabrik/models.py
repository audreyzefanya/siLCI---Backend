from django.db import models
from barang.models import Barang
import uuid

class Pabrik(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=50)
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
