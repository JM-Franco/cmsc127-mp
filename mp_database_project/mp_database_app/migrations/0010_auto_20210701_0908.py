# Generated by Django 3.1.7 on 2021-07-01 01:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp_database_app', '0009_auto_20210701_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='cooking_time',
        ),
        migrations.AddField(
            model_name='recipe',
            name='hours',
            field=models.IntegerField(default=1, null=True, validators=[django.core.validators.MaxValueValidator(24), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='recipe',
            name='minutes',
            field=models.IntegerField(default=1, null=True, validators=[django.core.validators.MaxValueValidator(60), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='serving',
            field=models.IntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
