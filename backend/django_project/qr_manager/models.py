from django.db import models

# Create your models here.
class QrCode(models.Model):
    data_created = models.DateField()
    date_finish = models.DateField()
    name = models.CharField(max_length=50)
    token = models.CharField(max_length=300)

    def __str__(self):
        return self.name