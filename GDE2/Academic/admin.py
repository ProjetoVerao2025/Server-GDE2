from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Attendance)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(CourseRequirement)
admin.site.register(Department)
admin.site.register(Enrollment)
admin.site.register(Professor)
admin.site.register(Program)
admin.site.register(Student)