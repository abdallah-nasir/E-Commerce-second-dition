# Generated by Django 3.2.4 on 2021-07-02 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STORE', '0026_auto_20210702_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='price_1',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]
