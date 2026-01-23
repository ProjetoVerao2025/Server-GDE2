from django.db import models

# Create your models here.

class Attendance(models.Model):
    class AttendanceStatus(models.IntegerChoices):
        Present = 1
        absent = 2
        excused = 3

    class_id = models.IntegerField()
    student_id = models.IntegerField()
    date = models.DateTimeField()
    status = models.IntegerField(choices = AttendanceStatus)
