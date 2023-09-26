from django.db import models

# Create your models here.
class QrCode(models.Model):
    date_created = models.DateField()
    date_finish = models.DateField() 
    name = models.CharField(max_length=50)
    token = models.CharField(max_length=300)
    senha = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class CustomVariable(models.Model):
    name = models.CharField(max_length=255)  # Name of the variable
    value = models.CharField(max_length=255)  # Value of the variable

    def __str__(self):
        return self.name