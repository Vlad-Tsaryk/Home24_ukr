# Generated by Django 3.2.15 on 2023-01-11 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_transaction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='persona_account',
            new_name='personal_account',
        ),
    ]