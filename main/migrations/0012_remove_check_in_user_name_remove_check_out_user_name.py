# Generated by Django 4.2 on 2023-06-15 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check_in',
            name='user_name',
        ),
        migrations.RemoveField(
            model_name='check_out',
            name='user_name',
        ),
    ]
