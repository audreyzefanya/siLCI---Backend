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

class JenisMerk(models.Model):
    nama = models.CharField(max_length=255, unique=True)
