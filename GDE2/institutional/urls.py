from django.contrib import admin
from django.urls import path, include
from .views import class_page, fetch_classes, fetch_courses

urlpatterns = [	
    path('classpage/', class_page),
	path('fetchclasses/', fetch_classes),
	path('fetchcourses/', fetch_courses)
]
