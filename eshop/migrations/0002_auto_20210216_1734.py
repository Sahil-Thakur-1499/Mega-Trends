# Generated by Django 3.1.6 on 2021-02-16 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
