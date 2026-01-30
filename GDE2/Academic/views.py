from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
from .models import *
import json


@csrf_exempt
def create_user(request :HttpRequest):
    payload = json.loads(request.body)

    if Student.objects.filter(ra = payload["ra"]).exists(): 
        return JsonResponse({"status": -1, "message": "Já existe um usuário com esse RA."}, status=400)


    try:
        program = Program.objects.get(id=payload["program_code"])
    except Program.DoesNotExist:
        return JsonResponse(
                {
                    "status": -1,
                    "message": f"Program {payload['program_code']} não existe."
                    },
                status=400
                )

    newUser = Student(
        ra = payload["ra"],
        name = payload["name"],
        program_code = program,
        level = payload["level"],
        password = make_password(payload["password"])
        )
    newUser.save()
    return JsonResponse({"status": 1, "message": "Criado com sucesso."})
