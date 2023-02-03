from django.db import models


# Create your models here.
class ExcelTemplate(models.Model):
    default = models.BooleanField(default=False)
    file = models.FileField()
    name = models.CharField(max_length=100)
