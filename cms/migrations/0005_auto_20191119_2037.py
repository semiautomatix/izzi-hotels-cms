# Generated by Django 2.2.7 on 2019-11-19 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20191119_1958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='type',
            new_name='service_type',
        ),
    ]
