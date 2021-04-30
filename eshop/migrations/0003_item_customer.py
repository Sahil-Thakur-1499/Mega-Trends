# Generated by Django 3.1.6 on 2021-04-22 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0002_auto_20210331_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='customer',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Customer2', to='eshop.customer'),
            preserve_default=False,
        ),
    ]
