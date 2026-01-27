from django.db import models

from django.contrib.auth.hashers import make_password

# Create your models here.

class Attendance(models.Model):
    class AttendanceStatus(models.IntegerChoices):
        Present = 1
        absent = 2
        excused = 3

    class_id = models.OneToOneField(
        "Academic.Class",
        on_delete = models.CASCADE
    )

    student_id = models.OneToOneField(
        "Academic.Student",
        on_delete = models.CASCADE
    )

    date = models.DateTimeField()
    status = models.IntegerField(choices = AttendanceStatus)

class Class(models.Model):  # sala específica (F159 Z)
    class ClassOffering(models.IntegerChoices): # Período em que a matéria é oferecida
        odd = 1
        even = 2
        sp = 3

    id = models.IntegerField(primary_key = True)
    course_code = models.OneToOneField(
        "Academic.Course",
        on_delete = models.CASCADE
    )
    letter = models.CharField()
    year_offered = models.IntegerField()
    period_offered = models.IntegerField(choices = ClassOffering)

    def __str__(self):
        return f"{self.class_code}({self.letter})"

class Course(models.Model): # matéria que você paga
    class CourseLevel(models.IntegerChoices): # nível de graduação
        Undergraduate = 1
        Graduate = 2

    class CourseOffering(models.IntegerChoices): # Período em que a matéria é oferecida
        odd = 1
        even = 2
        both = 3
        sp = 4

    id = models.IntegerField(primary_key = True)
    code = models.CharField(max_length = 5)
    name = models.CharField(max_length = 100)
    courseLevel = models.IntegerField(choices = CourseLevel) 
    department = models.IntegerField()
    credits = models.IntegerField()
    offered = models.IntegerField(choices = CourseOffering) 
    syllabus = models.CharField(max_length = 1000) # ementa

    def __str__(self):
        return f"{self.code}"
 
class CourseRequirement(models.Model): # prérequisitos (MC202 precisa de MC102)
    course_code = models.OneToOneField( # essa matéria depende
        "Academic.Course",
        on_delete = models.CASCADE,
            related_name = "course_code"
    )
    requirement_code = models.OneToOneField(
        "Academic.Course",
        on_delete = models.CASCADE,
        related_name = "requirement_code"
    ) # dessa

class Department(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    acronym = models.CharField(max_length = 10)

    def __str__(self):
        return f"{self.acronym}"

class Enrollment(models.Model):
    student_id = models.OneToOneField(
        "Academic.Student",
        on_delete = models.CASCADE
    )
    class_id = models.OneToOneField(
        "Academic.Class",
        on_delete = models.CASCADE
    )

class Professor(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.name}"

class Program(models.Model): # Curso que você cursa (CC == 42)
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return f"{self.name}"
    
class Student(models.Model):
    class StudentLevel(models.IntegerChoices):
        Undergraduate = 1  
        Graduate = 2
        Doctoral = 3
        Exchange = 4
        VisitingStudent = 5
    
    ra = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    program_code = models.OneToOneField(
        "Academic.Program",
        on_delete = models.CASCADE
    )
    level = models.IntegerField(choices = StudentLevel)
    password = models.CharField(max_length = 255, default = None)

    def __str__(self):
        return f"{self.ra:06d}"

    def save(self):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save()
