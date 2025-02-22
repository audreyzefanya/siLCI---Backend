# Generated by Django 5.0.2 on 2024-03-01 04:50

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barang', '0006_alter_perusahaanimpor_logo'),
        ('pabrik', '0006_alter_barangpabrik_id_barang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangpabrik',
            name='id_barang',
            field=models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='barang', serialize=False, to='barang.barang'),
        ),
    ]
