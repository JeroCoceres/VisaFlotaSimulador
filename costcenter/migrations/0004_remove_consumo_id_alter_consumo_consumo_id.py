# Generated by Django 5.0.3 on 2024-11-09 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costcenter', '0003_alter_distribution_id_alter_transaction_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumo',
            name='id',
        ),
        migrations.AlterField(
            model_name='consumo',
            name='consumo_id',
            field=models.BigIntegerField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
