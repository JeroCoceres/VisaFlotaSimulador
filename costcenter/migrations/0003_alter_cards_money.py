# Generated by Django 4.1.7 on 2023-03-22 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costcenter', '0002_alter_cards_options_alter_transaction_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cards',
            name='money',
            field=models.FloatField(default='0'),
        ),
    ]
