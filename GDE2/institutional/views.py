from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.db import models
from .models import *
from utils import _get_schedule, _get_current_period
from datetime import datetime
import json

# Create your views here.




def class_page(request: HttpRequest):
	try:
		payload = json.loads(request.body)
	except:
		return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})
	
	if "id" not in payload:
		return JsonResponse({"status": -1, "message": "Request não contém campo 'id'"})

	if not Class.objects.filter(id = payload["id"]).exists():
		return JsonResponse({"status": -1, "message": f"Turma com ID {payload['id']} não existe"})
	
	req_class = Class.objects.filter(id = payload["id"]).get()
	req_class_schedule = _get_schedule(req_class)

	course = req_class.course
	return JsonResponse({
		"status": 1,
		"message": "Turma encontrada",
		"course_code": course.code,
		"course_name": course.name,
		"class_letter": req_class.letter,
		"credits": course.credits,
		"year_offered": req_class.year_offered,
		"period_offered": req_class.period_offered,
		"schedule": req_class_schedule,
		"syllabus": course.syllabus

	})

def fetch_courses(request: HttpRequest):
	try:
		payload = json.loads(request.body)
	except:
		return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})

	if "criteria" not in payload:
		return JsonResponse({"status": -1, "message": "Request não contém campo 'criteria'"})

	if "body" not in payload:
		return JsonResponse({"status": -1, "message": "Request não contém campo 'body'"})

	if payload["criteria"] == "code":
		courses = Course.objects.filter(code__istartswith = payload["body"])

	elif payload["criteria"] == "name":
		courses = Course.objects.filter(name__icontains = payload["body"])

	elif payload["criteria"] == "department":
		courses = Course.objects.filter(department__name__icontains = payload["body"])

	else:
		return JsonResponse({"status": -1, "message": "Critério de busca inválido"})

	format_course = lambda x: {"id": x.id, "code": x.code, "name": x.name}
	courses = sorted(map(format_course, courses), key = lambda x: x["code"])
	if not courses:
		return JsonResponse({"status": -1, "message": "Nenhuma disciplina respeita o critério de busca"})

	return JsonResponse({"status": 1, "message": "Disciplinas encontradas", "courses": courses})

def fetch_classes(request: HttpRequest):
	try:
		payload = json.loads(request.body)
	except:
		return JsonResponse({"status": -1, "message": "Erro ao carregar o arquivo JSON"})

	if "id" not in payload:
		return JsonResponse({"status": -1, "message": "Request não contém campo 'id'"})
	
	try:
		fetched_course = Course.objects.filter(id = payload["id"]).get()
	except:
		return JsonResponse({"status": -1, "message": f"Curso com ID {payload['id']} não existe"})
	
	format_class = lambda x: {"letter": x.letter, "schedule": _get_schedule(x)}
	classes = sorted(
		map(
			format_class,
			Class.objects.filter(
				course = fetched_course.id,
				year_offered = datetime.now().year,
				period_offered = _get_current_period()
			)),
		key = lambda x: x["letter"]
	)
	if not classes:
		return JsonResponse({"status": -1, "message": f"Nenhuma turma de {fetched_course.code} nesse período"})

	return JsonResponse({"status": 1, "message": "Turmas encontradas", "classes": classes})

