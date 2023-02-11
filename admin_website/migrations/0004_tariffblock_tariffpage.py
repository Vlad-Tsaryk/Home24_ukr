# Generated by Django 3.2.15 on 2023-02-11 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_website', '0003_auto_20230211_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='TariffPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('text', models.TextField()),
                ('seo', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='admin_website.seo')),
            ],
        ),
        migrations.CreateModel(
            name='TariffBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='website/tariff_page/blocks')),
                ('title', models.CharField(max_length=70)),
                ('tariff_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_website.servicepage')),
            ],
        ),
    ]
