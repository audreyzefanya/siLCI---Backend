# Generated by Django 5.0.2 on 2024-02-29 16:56

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JenisGudang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='JenisMerk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gudang',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=255)),
                ('alamat', models.CharField(max_length=255)),
                ('kapasitas', models.BigIntegerField()),
                ('jenis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gudang.jenisgudang')),
            ],
        ),
    ]
