# Generated by Django 5.0.2 on 2024-03-01 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pabrik', '0004_alter_barangpabrik_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangpabrik',
            name='stok',
            field=models.IntegerField(default=0),
        ),
    ]
