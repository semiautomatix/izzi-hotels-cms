# Generated by Django 2.2.7 on 2019-11-28 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20191119_2037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='geo_location',
            new_name='geolocation',
        ),
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='hotelgroup',
            name='head_office_address',
            field=models.CharField(max_length=100),
        ),
    ]
