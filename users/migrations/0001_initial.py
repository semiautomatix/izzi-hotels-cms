# Generated by Django 2.2.7 on 2019-11-19 14:22

from django.conf import settings
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
            name='UserMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_range', models.TextField(choices=[('18', '18-24'), ('25', '25-34'), ('35', '35-44'), ('45', '45-54'), ('55', '55-64'), ('65', '65+')], max_length=100, null=True)),
                ('email_address', models.EmailField(max_length=254)),
                ('profile_picture', models.ImageField(null=True, upload_to='upload/images/')),
                ('user_type', models.TextField(choices=[('global', 'Global Administrator'), ('group', 'Hotel Group Administrator'), ('hotel', 'Hotel Administrator'), ('user', 'End User')], default='user', max_length=100)),
                ('middle_name', models.TextField(blank=True, max_length=100)),
                ('first_name', models.TextField(max_length=100)),
                ('last_name', models.TextField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('nationality', models.TextField(blank=True, max_length=100)),
                ('gender', models.TextField(choices=[('male', 'Male'), ('female', 'Female'), ('non_binary', 'Non binary')], max_length=100, null=True)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Hotel')),
                ('hotel_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.HotelGroup')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]