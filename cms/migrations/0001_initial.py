# Generated by Django 2.2.7 on 2019-11-19 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField()),
                ('adults', models.IntegerField(default=0)),
                ('start_date', models.DateField()),
                ('booking_status', models.TextField(choices=[('1', 'Confirmed'), ('0', 'Cancelled')], max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('children', models.PositiveIntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('geo_location', models.TextField(max_length=100)),
                ('postal_code', models.TextField(max_length=100)),
                ('country', models.TextField(max_length=100)),
                ('city', models.TextField(max_length=100)),
                ('hotel_name', models.TextField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('address', models.TextField(max_length=200)),
                ('logo', models.ImageField(upload_to='upload/images/')),
            ],
        ),
        migrations.CreateModel(
            name='HotelGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='upload/images/')),
                ('head_office_postal_code', models.TextField(max_length=100)),
                ('head_office_country', models.TextField(max_length=100)),
                ('hotel_group_name', models.TextField(max_length=100)),
                ('head_office_address', models.TextField(max_length=200)),
                ('head_office_city', models.TextField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('head_office_geolocation', models.TextField(blank=True, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='upload/images/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('icon_name', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.TextField(blank=True, max_length=100)),
                ('meeting_room', models.TextField(blank=True, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('type', models.TextField(choices=[('service', 'Service'), ('co_share', 'Co-share'), ('meeting_room', 'Meeting Room')], default='service', max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Hotel')),
                ('hotel_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.HotelGroup')),
                ('icon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Icon')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.TextField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='HotelGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='upload/images/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Hotel')),
            ],
        ),
    ]
