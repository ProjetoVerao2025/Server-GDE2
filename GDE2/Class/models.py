from django.db import models

# Create your models here.

class Class(models.Model):
    id = models.IntegerField(primary_key = True)
    class_code = models.IntegerField()
    letter = models.CharField()
