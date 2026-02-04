
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("login/", login_view),
    path("register/", register),
    path("logout/", logout_view),
    path("whoami/", whoami),
]

