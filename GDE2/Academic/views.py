from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .models import *
import json

def create_user(request :HttpRequest):
    payload = json.loads(request.body)

    if Student.objects.filter(ra = payload["ra"]).exists(): 
        return JsonResponse({"status": -1, "message": "Já existe um usuário com esse RA."})

    newUser = Student(
        ra = payload["ra"],
        name = payload["name"],
        program_code = payload["program_code"],
        level = payload["level"],
        password = make_password(payload["password"])
        )
    newUser.save()
    return JsonResponse({"status": 1, "message": "Criado com sucesso."})