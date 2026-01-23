from django.db import models

# Create your models here.

class Department(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length = 100)
    acronym = models.CharField(max_length = 10)