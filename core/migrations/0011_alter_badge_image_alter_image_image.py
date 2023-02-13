# Generated by Django 4.1.4 on 2023-02-13 20:27

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_badge_image_alter_image_image_alter_menu_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(), upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(), upload_to='images/'),
        ),
    ]
