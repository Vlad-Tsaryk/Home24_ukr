# Generated by Django 3.2.15 on 2023-02-07 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_role_purposes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
