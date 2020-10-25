# Generated by Django 2.2.7 on 2019-11-19 14:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.TextField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('end_date_time', models.DateTimeField()),
                ('created', models.DateTimeField()),
                ('event_metadata', models.TextField()),
                ('user', models.TextField(max_length=100)),
                ('start_date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('review', models.TextField(max_length=4000)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('check_out_date_time', models.DateTimeField(null=True)),
                ('end_date_time', models.DateTimeField()),
                ('check_in_date_time', models.DateTimeField(null=True)),
                ('start_date_time', models.DateTimeField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]