# Generated by Django 4.1.13 on 2024-01-03 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productattachment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productattachment',
            old_name='user',
            new_name='product',
        ),
    ]
