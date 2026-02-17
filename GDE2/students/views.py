from django.apps import apps
from django.http import HttpRequest, JsonResponse
from .models import *
from datetime import date, datetime, timedelta
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import logout, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from utils import _get_schedule, _get_enrolls
from institutional.models import Course, ClassSchedule


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
        for lesson in c.class_schedule.all():
            user_schedule.append((lesson.weekday, lesson.start_hour, lesson.start_hour + lesson.lesson_count, c.id))

    for new_class_lesson in new_class_schedule:
        for lesson in user_schedule:

            if lesson[0] == new_class_lesson[0] and not (lesson[1] >= new_class_lesson[2] or lesson[2] <= new_class_lesson[1]):
                conflicts.append(lesson)

    if conflicts:
        return JsonResponse({"status": -1, "message": "Horário indisponível.", "conflicts": conflicts})

    class_to_enroll = Class.objects.filter(id = payload["id"]).get()
    user = Student.objects.filter(ra = payload["ra"]).get()
    user.enrollments.add(class_to_enroll)
    return JsonResponse({"status": 1, "message": "Matéria matriculada com sucesso."})

def list_absences(request: HttpRequest):
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})

    if "ra" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'ra'"})

    if "id" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'id'"})

    user = Student.objects.filter(ra = payload["ra"])
    if not user.exists():
        return JsonResponse({"status": -1, "message": f"RA {payload['ra']} não cadastrado"})
    user = user.get()

    req_class = Class.objects.filter(id = payload["id"])
    if not req_class.exists():
        return JsonResponse({"status": -1, "message": f"Turma com ID {payload['id']} não existe"})
    req_class = req_class.get()

    if req_class not in user.enrollments.all():
        return JsonResponse({"status": -1, "message": f"{user} não está matriculado em {req_class}"})

    temp_func = lambda x: {"date": x.date}
    absences = list(map(temp_func, Attendance.objects.filter(academic_class = payload["id"], student = payload["ra"], status = 2)))
    return JsonResponse({"status": 1, "message": "Faltas encontradas", "absences": absences})

def fetch_attendance(request: HttpRequest):
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})

    if "ra" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'ra'"})

    if not Student.objects.filter(ra = payload["ra"]).exists():
        return JsonResponse({"status": -1, "message": f"RA {payload['ra']} não cadastrado"})

    temp_func = lambda x: {"date": x.date, "status": x.status, "class": x.academic_class}
    attendance = list(map(temp_func, Attendance.objects.filter(student = payload["ra"])))
    return JsonResponse({
        "status": 1,
        "message": "Presença encontrada",
        "attendance": attendance
    })

def edit_attendance(request: HttpRequest):
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})

    if "ra" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'ra'"})

    if "id" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'id'"})

    if "status" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'status'"})

    if "date" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'date'"})

    if "new_status" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'new_status'"})

    if not Student.objects.filter(ra = payload["ra"]).exists():
        return JsonResponse({"status": -1, "message": f"RA {payload['ra']} não cadastrado"})
    
    if not (payload["status"] >= 0 and payload["new_status"] <= 3):
        return JsonResponse({"status": -1, "message": f"Status {payload['status']} inválido"})
        
    try:
        day = date.fromisoformat(payload["date"])
    except Exception:
        return JsonResponse({"status": -1, "message": f"Falha ao coverter {payload["date"]} para objeto 'date'"})

    attendance = Attendance.objects.filter(student = payload["ra"], date = day, status = payload["status"], academic_class = payload["id"])
    if not attendance.exists():
        return JsonResponse({"status": -1, "message": f"Objeto 'Attendance' a ser editado não foi encontrado"})

    attendance.get()
    attendance.status = payload["new_status"]
    return JsonResponse({
        "status": 1,
        "message": f"Status de presença alterado para { payload['new_status'] }"
    })
        
def create_attendance(request: HttpRequest):
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})

    if "ra" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'ra'"})

    if "id" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'id'"})

    if "status" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'status'"})

    if "date" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'date'"})

    if "ignoreSchedule" not in payload:
        return JsonResponse({"status": -1, "message": "Request não contém campo 'ignoreSchedule'"})


    if not Student.objects.filter(ra = payload["ra"]).exists():
        return JsonResponse({"status": -1, "message": f"RA {payload['ra']} não cadastrado"})

    if not Student.objects.filter(ra = payload["ra"], enrollments = payload["id"]).exists()
        return JsonResponse({"status": -1, "message": f"Aluno de RA {payload['ra']} não matricualdo em matéria de ID {payload["id"]}"})

    if not Class.objects.filter(id = payload["id"]).exists():
        return JsonResponse({"status": -1, "message": f"Turma com ID {payload['id']} não existe"})

    try:
        day = date.fromisoformat(payload["date"])
    except Exception:
        return JsonResponse({"status": -1, "message": f"Falha ao coverter {payload["date"]} para objeto 'date'"})

    if not payload["ignoreSchedule"] and not ClassSchedule.objects.filter(weekday = day.weekday(), rclass = payload["id"]).exists():
        return JsonResponse({"status": -1, "message": f"Data ou horário inválidos"})

    Attendance(
        academic_class = payload["id"],
        student = payload["ra"],
        date = day,
        status = payload["status"]
        ).save()
    return JsonResponse({"status": 1, "message": "Presença marcada com sucesso"});

def update_presence(request: HttpRequest):
    day = date.today() - timedelta(days = 1)
    weekday = date.today().weekday()
    weekday = weekday if weekday else 7
    for class_schedule in ClassSchedule.objects.filter(weekday = weekday):
        for _class in Class.objects.filter(class_schedule = class_schedule):
            for student in Student.objects.filter(enrollments = _class):
                Attendance(
                    academic_class = _class,
                    student = student,
                    date = day,
                    status = 1
                ).save()
        
    for i in AttendanceIntent.objects.filter(date = day).exclude(id = 1):
        attendances = Attendance.objects.filter(
            academic_class = i.academic_class,
            student = i.student,
            date = day,
            status = 1
        )
        for a in attendances:
            a.status = i.status
            a.save()
    AttendanceIntent.objects.all().delete()
    return JsonResponse({"status": 1})
