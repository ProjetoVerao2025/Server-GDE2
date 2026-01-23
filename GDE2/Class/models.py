from django.db import models

# Create your models here.

class Class(models.Model):
    id = models.IntegerField()
    class_code = models.IntegerField()
    letter = models.CharField()
