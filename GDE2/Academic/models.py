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

class Class(models.Model):
    id = models.IntegerField(primary_key = True)
    class_code = models.IntegerField()
    letter = models.CharField()


class Course(models.Model):
    class CourseLevel(models.IntegerChoices):
        Undergraduate = 1
        Graduate = 2

    class CourseOffering(models.IntegerChoices):
        odd = 1
        even = 2
        both = 3
        sp = 4

    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length = 5)
    name = models.CharField(max_length = 100)
    CourseLevel = models.IntegerField(choices = CourseLevel) 
    department = models.IntegerField()
    credits = models.IntegerField()
    offered = models.IntegerField(choices = CourseOffering) 
    syllabus = models.CharField(max_length = 1000) #** n sei quanto exatamente colocar
 
class CourseRequirement(models.Model):
    course_code = models.IntegerField()
    requirement_code = models.IntegerField()

class Department(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    acronym = models.CharField(max_length = 10)

class Enrollment(models.Model):
    students = models.IntegerField()
    class_id = models.IntegerField()

class Professor(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)

class Program(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)

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

