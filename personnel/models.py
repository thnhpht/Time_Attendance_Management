from django.db import models


# Create your models here.


class Personnel(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/personnel')

    def __str__(self):
        return self.id + " " + self.name
