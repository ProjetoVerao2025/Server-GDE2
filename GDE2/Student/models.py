from django.db import models

# Create your models here.

class Student(models.Model):
    class StudentLevel(models.IntegerChoices):
        Undergraduate = 1  
        Graduate = 2
        Doctoral = 3
        Exchange = 4
        VisitingStudent = 5
    
    ra = models.IntegerField()
    name = models.CharField(max_length = 100)
    program_code = models.IntegerField()
    level = models.IntegerField(choices = StudentLevel)