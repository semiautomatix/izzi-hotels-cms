# Generated by Django 2.2.7 on 2019-11-29 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20191129_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='hotel_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cms.HotelGroup'),
            preserve_default=False,
        ),
    ]
