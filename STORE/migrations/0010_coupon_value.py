# Generated by Django 3.2.4 on 2021-07-26 11:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STORE', '0009_auto_20210726_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='value',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
