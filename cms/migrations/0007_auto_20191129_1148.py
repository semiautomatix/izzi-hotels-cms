# Generated by Django 2.2.7 on 2019-11-29 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20191128_1331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='Hotel',
            new_name='hotel',
        ),
    ]
