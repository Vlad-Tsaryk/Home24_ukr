# Generated by Django 3.2.15 on 2022-11-20 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_house', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='date_edit',
            field=models.DateTimeField(auto_now=True),
        ),
    ]