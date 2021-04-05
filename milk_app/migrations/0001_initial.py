# Generated by Django 3.1.7 on 2021-04-05 04:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import milk_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to=milk_app.models.generate_filename_userpic)),
                ('account', models.CharField(choices=[(None, ''), ('Host', 'Host'), ('Tenant', 'Tenant')], help_text='Note: You must provide a valid Student email to Register as a Tenant', max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('listing_id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=500)),
                ('price', models.IntegerField(null=True)),
                ('address', models.CharField(max_length=100)),
                ('rating', models.IntegerField(null=True)),
                ('picture', models.ImageField(upload_to=milk_app.models.generate_filename_listing)),
                ('date', models.DateField(default=datetime.date.today)),
                ('university', models.CharField(max_length=40)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='milk_app.userprofile')),
            ],
            options={
                'verbose_name_plural': 'Listings',
            },
        ),
    ]
