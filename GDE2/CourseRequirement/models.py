from django.db import models

# Create your models here.

class CourseRequirement(models.Model):
    course_code = models.IntegerField()
    requirement_code = models.IntegerField()