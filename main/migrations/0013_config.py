# Generated by Django 4.2 on 2023-06-22 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_check_in_user_name_remove_check_out_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wifi', models.CharField(max_length=200)),
                ('location_id', models.CharField(max_length=50)),
                ('location_add', models.CharField(max_length=200)),
            ],
        ),
    ]
