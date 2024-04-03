# Generated by Django 5.0.2 on 2024-02-28 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barang', '0003_alter_barang_merk'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerusahaanImpor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50)),
                ('deskripsi', models.TextField()),
                ('listBarang', models.ManyToManyField(blank=True, to='barang.barang')),
            ],
        ),
    ]
