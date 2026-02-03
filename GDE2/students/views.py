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
        user = Student.objects.filter(ra = payload["ra"]).get()
        full_schedule = []
        schedule = ClassSchedule.objects.filter(class__id = payload["id"])
        for h in schedule:
            full_schedule.append((h.weekday, h.start_hour, h.start_hour + h.lesson_count))

        conflicts = []
        for c in Class.objects.filter(student__ra = payload["ra"]):
            schedule = ClassSchedule.objects.filter(class__id = c.id)
            for h in schedule:
                end = h.start_hour + h.lesson_count
                if full_schedule[0] == h.weekday and (full_schedule[1] <= end or full_schedule[2] >= h.start_hour):
                    conflicts.append([h.weekday, h.start_hour, c.id])

        if conflicts:
            return JsonResponse({"status": -1, "message": "Horário indisponível.", "conflicts": conflicts})

        class_to_enroll = Class.objects.filter(id = payload["id"]).get()
        user.enrollments.add(class_to_enroll)
        return JsonResponse({"status": 1, "message": "Matéria matriculada com sucesso."})

    return JsonResponse({"status": -1, "message": "RA não cadastrado."})

# def fecth_home(request: HttpRequest):
    # payload = json.loads(request.body)
    # if "ra" not in payload:
        # return JsonResponse({"status": -1, "message": "RA não cadastrado")
    # elif:













