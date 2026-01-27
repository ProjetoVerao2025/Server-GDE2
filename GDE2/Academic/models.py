from django.db import models

from django.contrib.auth.hashers import make_password

# Create your models here.

class Attendance(models.Model):
    class AttendanceStatus(models.IntegerChoices):
        Present = 1
        Absent = 2
        Excused = 3

    academic_class = models.ForeignKey(
        "Academic.Class",
        to_field='id',
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        "Academic.Student",
        to_field='ra',
        on_delete=models.CASCADE
    )

    date = models.DateTimeField()
    status = models.IntegerField(choices=AttendanceStatus)

    class Meta:
        unique_together = ("academic_class", "student", "date")

class Class(models.Model):  # turma específica (F159 Z)
    class ClassOffering(models.IntegerChoices): # Período em que a matéria é oferecida
        odd = 1
        even = 2
        sp = 3

    id = models.IntegerField(primary_key = True)
    course = models.ForeignKey(
        "Academic.Course",
        on_delete = models.CASCADE
    )
    letter = models.CharField(max_length=1)
    year_offered = models.IntegerField()
    period_offered = models.IntegerField(choices=ClassOffering)

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
    course_code = models.ForeignKey( # essa matéria depende
        "Academic.Course",
        on_delete = models.CASCADE,
        to_field='id',
        related_name="Course"
    )
    requirement_code = models.ForeignKey(
        "Academic.Course",
        on_delete = models.CASCADE,
        related_name="Requirement"
    ) # dessa

class Department(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    acronym = models.CharField(max_length = 10)

    def __str__(self):
        return f"{self.acronym}"


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
    program_code = models.ForeignKey(
        "Academic.Program",
        on_delete = models.CASCADE
    )
    level = models.IntegerField(choices = StudentLevel)
    email = models.CharField(max_length = 255, null=True)
    password = models.CharField(max_length = 255, null=True)

    def __str__(self):
        return f"{self.ra:06d}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Enrollment(models.Model):
    student = models.ForeignKey(
        "Academic.Student",
        on_delete=models.CASCADE,
        to_field="ra"
        
    )
    academic_class = models.ForeignKey(
        "Academic.Class",
        to_field='id',
        on_delete=models.CASCADE
    )


class ClassLocation(models.Model): # Salas de aula
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.TextField()
    capacity = models.IntegerField()
    building = models.TextField()
    floor = models.IntegerField()


class ClassSchedule(models.Model): # Horarios das aulas das turmas
    class Weekdays(models.IntegerChoices):
        Monday = 1
        Tuesday = 2
        Wednesday = 3
        Thursday = 4
        Friday = 5
        Saturday = 6
        Sunday = 7

    weekday = models.IntegerField(choices=Weekdays)
    start_hour = models.IntegerField()
    lesson_count = models.IntegerField()
    
    # Sala onde a aula ocorre
    location = models.ForeignKey(
        "Academic.ClassLocation", 
        on_delete=models.CASCADE,
    )
