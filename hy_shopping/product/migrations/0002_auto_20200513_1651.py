# Generated by Django 3.0.6 on 2020-05-13 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stuck',
            new_name='stock',
        ),
    ]