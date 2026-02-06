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
from utils import _get_schedule, _get_enrolls
from institutional.models import Course


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


def fetch_home(request: HttpRequest): #só recebe o ra no json, retorna nome, matricula(horários, local, acronimo e letra) e hor
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})
    
    if "ra" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'ra'"})
    
    user = Student.objects.filter(ra = payload["ra"])
    if not user.exists():
        return JsonResponse({"status": -1, "message": f"RA {payload['ra']} não cadastrado"})

    user = user.get()
    enrolls = _get_enrolls(user)

    return JsonResponse({
        "status": 1,
        "message": "Deu tudo certo ao buscar as informações da home",
        "enrollments": enrolls,
        "name": user.name
    })

def fetch_profile_infos(request: HttpRequest):
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})
    if "ra" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'ra'"})
    user = Student.objects.filter(payload["ra"])
    if not user.exists():
        return JsonResponse({"status": -1, "message": f"RA {payload['ra']} não cadastrado"})
    
    user = user.get()
    course_name = Course.objects.filter(id = user.program_code)
    return JsonResponse({"status": 1,
                        "message": "Deu certo ao procurar as informações do perfil",
                        "course": course_name,
                        "ra": user.ra,
                        "name": user.name,
                        "credits":user.credits
                        })

def fetch_enrollments(request: HttpRequest):
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})
    if "ra" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'ra'"})
    user = Student.objects.filter(ra = payload["ra"])
    if not user.exists():
        return JsonResponse({"status": -1, "message": f"RA {payload['ra']} não cadastrado"})
    
    user = user.get()
    enrolls = _get_enrolls(user)
    return JsonResponse({"status": 1,
                        "message": "Deu tudo certo ao buscar informações das matrículas do estudante",
                        "enrollments": enrolls})


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
	"""
	Receives a JSON with the RA of the enrolling student and the ID of the class in which to enroll.
	Returns a JSON with a STATUS (-1 for Error and 1 for Success) and a MESSAGE
	"""
	try:
		payload = json.loads(request.body)
	except:
		return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})

	if "ra" not in payload:
		return JsonResponse({"status": -1, "message": "Request não contém campo 'ra'"})

	if "id" not in payload:
		return JsonResponse({"status": -1, "message": "Request não contém campo 'id'"})

	if not Student.objects.filter(ra = payload["ra"]).exists():
		return JsonResponse({"status": -1, "message": f"RA {payload['ra']} não cadastrado"})

	if not Class.objects.filter(id = payload["id"]).exists():
		return JsonResponse({"status": -1, "message": f"Turma com ID {payload['id']} não existe"})

	new_class_schedule = []
	schedule = ClassSchedule.objects.filter(class__id = payload["id"])
	for lesson in schedule:
		new_class_schedule.append((lesson.weekday, lesson.start_hour, lesson.start_hour + lesson.lesson_count))

	conflicts = []
	user_schedule = []
	for c in Class.objects.filter(student__ra = payload["ra"]):
		schedule = ClassSchedule.objects.filter(class__id = c.id)
		for lesson in schedule:
			user.append((lesson.weekday, lesson.start_hour, lesson.start_hour + lesson.lesson_count, c.id))

	for new_class_lesson in new_class_schedule:
		for lesson in user_schedule:
			if lesson[0] == new_class_lesson[0] and not (lesson[1] >= new_class_lesson[2] or lesson[2] <= new_class_lesson[1]):
				conflicts.append([h.weekday, h.start_hour, lesson[3]])

	if conflicts:
		return JsonResponse({"status": -1, "message": "Horário indisponível.", "conflicts": conflicts})

	class_to_enroll = Class.objects.filter(id = payload["id"]).get()
	user = Student.objects.filter(ra = payload["ra"]).get()
	user.enrollments.add(class_to_enroll)
	return JsonResponse({"status": 1, "message": "Matéria matriculada com sucesso."})

