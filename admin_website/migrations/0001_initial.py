# Generated by Django 3.2.15 on 2023-02-11 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SEO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('keywords', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='website/main_page')),
                ('image2', models.ImageField(upload_to='website/main_page')),
                ('image3', models.ImageField(upload_to='website/main_page')),
                ('text', models.TextField()),
                ('title', models.CharField(max_length=70)),
                ('show_app_urls', models.BooleanField(default=True)),
                ('seo', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='admin_website.seo')),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('main_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_website.mainpage')),
            ],
        ),
    ]