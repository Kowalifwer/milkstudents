# Generated by Django 2.2.17 on 2021-04-03 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('account', models.CharField(choices=[(None, ''), ('Host', 'Host'), ('Tenant', 'Tenant')], help_text='What kind of account is this?', max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('listing_id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=500)),
                ('price', models.IntegerField(null=True)),
                ('address', models.CharField(max_length=100)),
                ('rating', models.IntegerField(null=True)),
                ('picture', models.ImageField(upload_to='listing_images')),
                ('date', models.DateField(null=True)),
                ('uniName', models.CharField(max_length=40)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='milk_app.UserProfile')),
            ],
            options={
                'verbose_name_plural': 'Listings',
            },
        ),
    ]
