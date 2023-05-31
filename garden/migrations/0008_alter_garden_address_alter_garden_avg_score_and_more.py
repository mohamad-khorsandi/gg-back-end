# Generated by Django 4.2 on 2023-05-31 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0007_alter_garden_garden_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garden',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='garden',
            name='avg_score',
            field=models.FloatField(blank=True, default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='garden',
            name='business_code',
            field=models.CharField(blank=True, max_length=12, validators=[django.core.validators.MinLengthValidator(12)]),
        ),
        migrations.AlterField(
            model_name='garden',
            name='is_verified',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='garden',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='garden',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, validators=[django.core.validators.MinLengthValidator(11)]),
        ),
    ]
