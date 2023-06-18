# Generated by Django 3.2.15 on 2023-03-21 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("admin_service", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tariff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        error_messages={"unique": "Тариф із таким ім'ям вже існує!"},
                        max_length=50,
                        unique=True,
                    ),
                ),
                ("description", models.TextField()),
                ("date_edit", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-date_edit"],
            },
        ),
        migrations.CreateModel(
            name="TariffService",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.FloatField()),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admin_service.service",
                    ),
                ),
                (
                    "tariff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admin_tariff.tariff",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="tariff",
            name="services",
            field=models.ManyToManyField(
                through="admin_tariff.TariffService", to="admin_service.Service"
            ),
        ),
    ]
