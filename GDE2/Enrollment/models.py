from django.db import models

# Create your models here.

class Enrollment(models.Model):
    students = models.IntegerField()
    class_id = models.IntegerField()
