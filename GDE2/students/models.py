from django.db import models
from institutional.models import Class, Program
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your models here.

class Attendance(models.Model):
    class AttendanceStatus(models.IntegerChoices):
        Present = 1
        Absent = 2
        Excused = 3

    academic_class = models.ForeignKey(
        "institutional.Class",
        to_field='id',
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        "students.Student",
        to_field='ra',
        on_delete=models.CASCADE
    )

    date = models.DateTimeField()
    status = models.IntegerField(choices=AttendanceStatus)

    class Meta:
        unique_together = ("academic_class", "student", "date")


    def __str__(self):
        return f"{self.class_code}({self.letter})"

class Student(models.Model):
    class StudentLevel(models.IntegerChoices):
        Undergraduate = 1  
        Graduate = 2
        Doctoral = 3
        Exchange = 4
        VisitingStudent = 5

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    enrollments = models.ManyToManyField(Class, blank= True)  
    ra = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    program_code = models.ForeignKey(
        "institutional.Program",
        on_delete = models.CASCADE
    )
    level = models.IntegerField(choices = StudentLevel)

    def __str__(self):
        return f"{self.ra:06d}"


