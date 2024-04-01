from django.db import models

import uuid
from authentication.models import CustomUser

class Merk(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length = 50, unique=True)

class Barang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merk = models.ForeignKey('Merk', on_delete=models.CASCADE, null=True, related_name='barang')
    nama = models.CharField(max_length = 50, null = False, unique=True)
    deskripsi = models.TextField()
    harga = models.BigIntegerField()

class PerusahaanImpor(models.Model):
    nama = models.CharField(max_length = 50, unique=True)
    deskripsi = models.TextField()
    logo = models.TextField(null=True, blank=True)
    listBarang = models.ManyToManyField(Barang, blank=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.PROTECT, related_name='perusahaan', null=True, blank=True)

class PengadaanBarangImpor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    perusahaan = models.ForeignKey(PerusahaanImpor, on_delete=models.CASCADE, default=uuid.uuid4)
    barang = models.ForeignKey('barang.Barang', on_delete=models.CASCADE, default=uuid.uuid4)
    jumlahBarang = models.IntegerField()
    gudangTujuan = models.ForeignKey('gudang.Gudang', on_delete=models.CASCADE, default=uuid.uuid4)
    totalHarga = models.BigIntegerField()
    tanggalPermintaaan = models.DateTimeField(auto_now_add=True)
    tanggalUpdate = models.DateTimeField(auto_now=True)
    fileInvoice = models.TextField(null=True, blank=True)
    filePayment = models.TextField(null=True, blank=True)



