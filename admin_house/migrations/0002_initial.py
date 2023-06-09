# Generated by Django 3.2.15 on 2023-03-21 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("admin_house", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="houseuser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="house",
            name="users",
            field=models.ManyToManyField(
                through="admin_house.HouseUser", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="floor",
            name="house",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="admin_house.house"
            ),
        ),
    ]
