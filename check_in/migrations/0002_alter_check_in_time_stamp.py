# Generated by Django 4.2 on 2023-04-20 06:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_in', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check_in',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]