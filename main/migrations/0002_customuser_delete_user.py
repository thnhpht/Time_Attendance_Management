# Generated by Django 4.2 on 2023-05-25 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('tel', models.CharField(max_length=10)),
                ('image', models.ImageField(upload_to='images/user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
