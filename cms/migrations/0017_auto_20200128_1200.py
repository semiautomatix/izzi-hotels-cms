# Generated by Django 2.2 on 2020-01-28 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20200127_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='rooms',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='booking',
            name='adults',
            field=models.IntegerField(default=1),
        ),
    ]