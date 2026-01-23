from django.db import models

# Create your models here.

class Program(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length = 100)
