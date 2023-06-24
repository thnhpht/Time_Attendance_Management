from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, email, name, tel, image, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, tel=tel, image=image, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email=None, name=None, tel=None, image=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, tel, image, password, **extra_fields)

    def create_superuser(self, email=None, name=None, tel=None, image=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, name, tel, image, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/user')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split('@')[0]


class Check_In(models.Model):
    user_id = models.CharField(max_length=10)
    date = models.DateField(default=datetime.now)
    time = models.TimeField(default=datetime.now)

    def __str__(self):
        return "ID: " + self.user_id + " - Date: " + str(self.date) + " - Time: " + str(self.time)

class Check_Out(models.Model):
    user_id = models.CharField(max_length=10)
    date = models.DateField(default=datetime.now)
    time = models.TimeField(default=datetime.now)

    def __str__(self):
        return "ID: " + self.user_id + " - Date: " + str(self.date) + " - Time: " + str(self.time)

class Config(models.Model):
    location_add = models.CharField(max_length=255)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    wifi = models.CharField(max_length=50)

    def __str__(self):
        return "Address: " + str(self.location_add) + " - Wifi: " + str(self.wifi)