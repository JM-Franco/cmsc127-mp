# Generated by Django 3.1.7 on 2021-07-01 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp_database_app', '0008_auto_20210701_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='last_modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='last_modified',
            field=models.DateTimeField(null=True),
        ),
    ]
