# Generated by Django 3.2.4 on 2021-07-02 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('STORE', '0024_alter_filter_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='STORE.category'),
        ),
    ]
