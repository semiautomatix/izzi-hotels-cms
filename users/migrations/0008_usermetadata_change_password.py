# Generated by Django 2.2 on 2020-02-11 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_usermetadata_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermetadata',
            name='change_password',
            field=models.BooleanField(default=True),
        ),
    ]
