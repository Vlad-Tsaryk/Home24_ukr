# Generated by Django 3.2.15 on 2023-02-08 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20230208_1622'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]