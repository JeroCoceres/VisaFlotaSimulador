# Generated by Django 5.0.3 on 2024-11-15 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costcenter', '0010_alter_consumo_clase_alter_consumo_tipo_de_gasto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_fullname',
            field=models.CharField(default=245, max_length=30),
            preserve_default=False,
        ),
    ]
