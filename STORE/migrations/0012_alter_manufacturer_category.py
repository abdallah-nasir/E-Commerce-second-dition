# Generated by Django 3.2.4 on 2021-07-29 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('STORE', '0011_alter_coupon_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='STORE.category'),
        ),
    ]
