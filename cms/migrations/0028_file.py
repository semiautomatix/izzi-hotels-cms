# Generated by Django 2.2 on 2020-07-20 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0027_auto_20200331_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
            ],
        ),
    ]
