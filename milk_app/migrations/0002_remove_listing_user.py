# Generated by Django 2.2.17 on 2021-04-01 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('milk_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='user',
        ),
    ]