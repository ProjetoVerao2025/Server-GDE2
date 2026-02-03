from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Class)
admin.site.register(ClassLocation)
admin.site.register(ClassSchedule)
admin.site.register(Course)
admin.site.register(CourseRequirement)
admin.site.register(Department)
admin.site.register(Professor)
admin.site.register(Program)
