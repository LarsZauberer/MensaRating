# Generated by Django 4.1.4 on 2023-05-12 08:55

import datetime
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_merge_20230302_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Memes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('img', models.ImageField(storage=django.core.files.storage.FileSystemStorage(), upload_to='images/')),
                ('text', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.AlterField(
            model_name='menu',
            name='date',
            field=models.DateField(default=datetime.date(2023, 5, 12)),
        ),
    ]