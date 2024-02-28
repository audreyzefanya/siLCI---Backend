from django.db import models
import uuid

class Merk(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length = 50)

class Barang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merk = models.ForeignKey('Merk', on_delete=models.CASCADE, null=True, related_name='barang')
    nama = models.CharField(max_length = 50, null = False)
    deskripsi = models.TextField()
    harga = models.BigIntegerField()

class PerusahaanImpor(models.Model):
    nama = models.CharField(max_length = 50)
    deskripsi = models.TextField()
    listBarang = models.ManyToManyField(Barang, blank=True)



