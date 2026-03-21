
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register, name = "register"),
    path("logout/", logout_view, name = "logout"),
    path("whoami/", whoami, name = "whoami"),
    path("enroll/", enroll_student, name = "enroll"),
    path("list-absences/", list_absences, name = "absences"),
    path("notifications/", notify_user, name = "notifications")    ,
    path("report/", special_dates, name = "special_dates")


    #temporary endpoint for API testing
    path("updatedb/", update_presence)
]

