from django.db import models

import uuid
from authentication.models import CustomUser
from cloudinary.models import CloudinaryField

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
    nama = models.CharField(max_length = 50)
    deskripsi = models.TextField()
    logo = models.TextField(null=True, blank=True)
    listBarang = models.ManyToManyField(Barang, blank=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.PROTECT, related_name='perusahaan', null=True, blank=True)


