# Generated by Django 3.2.4 on 2021-07-02 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('STORE', '0027_alter_filter_price_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='color',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='STORE.color'),
        ),
    ]
