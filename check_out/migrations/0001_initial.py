# Generated by Django 4.2 on 2023-04-20 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check_Out',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personnel_id', models.CharField(max_length=10)),
                ('personnel_name', models.CharField(max_length=255)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]