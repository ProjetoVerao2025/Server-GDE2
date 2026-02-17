from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Attendance)
admin.site.register(AttendanceIntent)
admin.site.register(Student)
