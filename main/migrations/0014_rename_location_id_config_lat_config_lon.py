# Generated by Django 4.2 on 2023-06-23 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_config'),
    ]

    operations = [
        migrations.RenameField(
            model_name='config',
            old_name='location_id',
            new_name='lat',
        ),
        migrations.AddField(
            model_name='config',
            name='lon',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
