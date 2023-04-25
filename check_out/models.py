from datetime import datetime
from django.db import models


# Create your models here.


class Check_Out(models.Model):
    personnel_id = models.CharField(max_length=10)
    personnel_name = models.CharField(max_length=255)
    date = models.DateField(default=datetime.now)
    time = models.TimeField(default=datetime.now)

    def __str__(self):
        return self.personnel_id + " " + self.personnel_name + " " + str(self.date) + " " + str(self.time)
