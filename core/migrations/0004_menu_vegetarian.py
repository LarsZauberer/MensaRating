# Generated by Django 4.1.4 on 2023-01-30 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_menu_menutype'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='vegetarian',
            field=models.BooleanField(default=False),
        ),
    ]