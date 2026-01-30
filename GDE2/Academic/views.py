from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.db import models
from .models import *
from datetime import *
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

def enroll_student(request: HttpRequest):
    payload = json.loads(request.body)

    if Student.objects.filter(ra = payload["ra"]).exists():
        placeholder = Class.objects.filter(id = payload["id"]).get()
        user = Student.objects.filter(ra = payload["ra"]).get()
        sch = []
        schedule = ClassSchedule.objects.filter(class__id = payload["id"])
        for h in schedule:
            sch.append((h.weekday, h.start_hour, h.start_hour + h.lesson_count))

        conflicts = []
        for c in Class.objects.filter(student__ra = payload["ra"]):
            schedule2 = ClassSchedule.objects.filter(class__id = c.id)
            for h in schedule2:
                end = h.start_hour + h.lesson_count
                if sch[0] == h.weekday and (sch[1] <= end or sch[2] >= h.start_hour):
                    conflicts.append([h.weekday, h.start_hour, c.id])
            
        if conflicts:
            return JsonResponse({"status": -1, "message": "Horário indisponível.", "conflicts": conflicts})
        
        user.enrollments.add(placeholder)
        return JsonResponse({"status": 1, "message": "Matéria matriculada com sucesso."})
    
    return JsonResponse({"status": -1, "message": "RA não cadastrado."})

