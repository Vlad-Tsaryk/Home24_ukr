# Generated by Django 3.2.15 on 2023-02-03 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_templates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exceltemplate',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
