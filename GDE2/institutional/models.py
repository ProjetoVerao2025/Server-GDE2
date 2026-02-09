from django.db import models

# Create your models here.
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
    

class Enrollment(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        to_field="ra"
        
    )

    academic_class = models.ForeignKey(
        "institutional.Class",
        to_field='id',
        on_delete=models.CASCADE
    )
    def __str__(self):
        return f"{self.student.ra} {str(self.academic_class)}"


class ClassLocation(models.Model): # Salas de aula
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.TextField()
    capacity = models.IntegerField()
    building = models.TextField()
    floor = models.IntegerField() 

    def __str__(self):
        return f"{self.building}"

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
        "institutional.ClassLocation", 
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return f"{self.weekday} {self.start_hour}-{self.start_hour + self.lesson_count} {str(self.location)}"
class Class(models.Model):  # turma específica (F159 Z)
    class ClassOffering(models.IntegerChoices): # Período em que a matéria é oferecida
        odd = 1
        even = 2
        sp = 3

    id = models.IntegerField(primary_key = True)

    course = models.ForeignKey(
        "institutional.Course",
        on_delete = models.CASCADE
    )
    letter = models.CharField(max_length=1)
    year_offered = models.IntegerField()
    period_offered = models.IntegerField(choices = ClassOffering)
    class_schedule = models.ManyToManyField(ClassSchedule)

    def __str__(self):
        return f"{self.course.code} {self.letter} {self.year_offered} {self.period_offered}"

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
    department = models.ForeignKey(
		"institutional.Department",
		on_delete = models.CASCADE
	)
    credits = models.IntegerField()
    offered = models.IntegerField(choices = CourseOffering) 
    syllabus = models.CharField(max_length = 1000) # ementa

    def __str__(self):
        return f"{self.code}"
 
class CourseRequirement(models.Model): # prérequisitos (MC202 precisa de MC102)
    course_code = models.ForeignKey( # essa matéria depende
        "institutional.Course",
        on_delete = models.CASCADE,
        to_field='id',
        related_name="Course"
    )
    requirement_code = models.ForeignKey(
        "institutional.Course",
        on_delete = models.CASCADE,
        related_name="Requirement"
    ) # dessa
