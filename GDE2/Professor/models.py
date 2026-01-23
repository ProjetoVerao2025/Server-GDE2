from django.db import models

# Create your models here.

class Professor(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length = 100)
