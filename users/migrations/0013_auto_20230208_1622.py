# Generated by Django 3.2.15 on 2023-02-08 14:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.AddField(
            model_name='message',
            name='receivers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]