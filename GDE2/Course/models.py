from django.db import models

# Create your models here.

class Course(models.Model):
    class CourseLevel(models.IntegerChoices):
        Undergraduate = 1
        Graduate = 2

    class CourseOffering(models.IntegerChoices):
        odd = 1
        even = 2
        both = 3
        sp = 4

    id = models.IntegerField()
    code = models.CharField(max_length = 5)
    name = models.CharField(max_length = 100)
    CourseLevel = models.IntegerField(choices = CourseLevel) 
    department = models.IntegerField()
    credits = models.IntegerField()
    offered = models.IntegerField(choices = CourseOffering) 
    syllabus = models.CharField(max_length = 1000) #** n sei quanto exatamente colocar
 