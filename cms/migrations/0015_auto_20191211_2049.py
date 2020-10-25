# Generated by Django 2.2 on 2019-12-11 18:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_auto_20191211_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='max_persons',
            field=models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)]),
        ),
        migrations.AddField(
            model_name='room',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]