# Generated by Django 5.0.4 on 2024-05-12 16:19

import eshopapp.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshopapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', eshopapp.models.CustomUserManager()),
            ],
        ),
    ]
