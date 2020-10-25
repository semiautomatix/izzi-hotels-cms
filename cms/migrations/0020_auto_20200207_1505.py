# Generated by Django 2.2 on 2020-02-07 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0019_auto_20200205_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='ibe_domain',
            field=models.CharField(max_length=100, null=True, verbose_name='IBE Domain'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='ibe_id',
            field=models.IntegerField(null=True, verbose_name='IBE Id'),
        ),
    ]
