# Generated by Django 5.0.2 on 2024-05-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barang', '0019_alter_pengadaanbarangimpor_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='barang',
            name='foto',
            field=models.TextField(blank=True, null=True),
        ),
    ]
