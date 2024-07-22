# Generated by Django 5.0.3 on 2024-07-20 18:20

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_costcenter', models.BooleanField(default=False)),
                ('card_name', models.CharField(max_length=20)),
                ('card_number', models.BigIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1000000000000000), django.core.validators.MaxValueValidator(9999999999999999)])),
                ('money', models.FloatField(default=0.0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Card',
                'verbose_name_plural': 'Cards',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('from_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_transactions', to='costcenter.cards')),
                ('to_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_transactions', to='costcenter.cards')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]
