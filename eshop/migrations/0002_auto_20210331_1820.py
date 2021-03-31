# Generated by Django 3.1.6 on 2021-03-31 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(to='eshop.Item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]