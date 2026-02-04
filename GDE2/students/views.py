from django.apps import apps
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.db import models
from .models import *
from datetime import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import logout, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate



# Debug ony: Usado durante o desenvolvimento para verificar
# Se a autenticacao estava funcionando corretamente
@csrf_exempt
@require_GET
def whoami(request:HttpRequest):
    if request.user.is_authenticated:
        return JsonResponse({"status": 0, "message": request.user.get_username()})
    return JsonResponse({"status": 0, "message": "user unknown"})




@csrf_exempt
@require_POST
def logout_view(request:HttpRequest):
    logout(request)
    print('rebolei leintiho')
    return JsonResponse({"status": -1, "message": "Logout realizado com sucesso!"})



@csrf_exempt
@require_POST
def register(request :HttpRequest):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": -1, "message": "Formato invalido. Payload apenas em JSON."})

    
    if Student.objects.filter(ra = payload["ra"]).exists():
        return JsonResponse({"status": -1, "message": "Já existe um usuário com esse RA."})
    
    Program = apps.get_model("institutional", "Program")

    try:
        program = Program.objects.get(id=payload["program_code"])
    except ObjectDoesNotExist:
        return JsonResponse({"status": -1, "message": f"Nao existe curso com id {payload['program_code']}"})


    try:
        level = Student.StudentLevel[payload["level"]]
    except KeyError:
        return JsonResponse({"status": -1, "message": f"Valor do campo level invalido. Valores validos: Undergraduate, Graduate, Doctoral, Exchange, VisitingStudent"})

    newUser = User.objects.create_user(
        username=payload["ra"],
        email=payload["email"],
        password=payload["password"],
    )

        

    Student.objects.create(
        ra = payload["ra"],
        name = payload["name"],
        level = level,
        program_code = program,
        user=newUser
        )

    return JsonResponse({"status": 0, "message": "Criado com sucesso."})


@csrf_exempt
@require_POST
def login_view(request: HttpRequest):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": -1, "message": "Formato invalido. Payload apenas em JSON."})

    ra = payload.get("ra")
    password = payload.get("password")

    if not ra or not password:
        return JsonResponse(
            {"status": -1, "message": "RA e senha são obrigatórios"},
            status=400
        )

    try:
        student = Student.objects.get(ra=ra)
    except ObjectDoesNotExist:
        return JsonResponse(
            {"status": -1, "message": "Credenciais inválidas"},
            status=401
        )

    user = authenticate(
        request,
        username=ra,
        password=password
    )

    if user is None:
        return JsonResponse(
            {"status": -1, "message": "Credenciais inválidas"},
            status=401
        )

    login(request, user)
    return JsonResponse({"status": 0, "message": "Logged in"})




@csrf_exempt
@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"ok": True})


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
