# Generated by Django 3.2.4 on 2021-07-04 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STORE', '0034_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='show',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='filter',
            name='sort',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
