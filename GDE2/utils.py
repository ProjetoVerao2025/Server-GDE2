from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.db import models
# from .models import *
from datetime import datetime
import json

def _get_schedule(_class: Class):
	return sorted(
		map(
			lambda x: {
				"weekday": x.weekday,
				"start_hour": x.start_hour,
				"lesson_count": x.lesson_count,
				"location": ClassLocation.objects.filter(id = x.location).get().building
			},
			_class.class_schedule.all()
		),
		key = lambda x: (x["weekday"], x["starthour"])
	)
		
def _get_current_period():
	month = datetime.now().month
	if month in (2, 3, 4, 5):
		return 1

	if month in (8, 9, 10, 11):
		return 2

	return 3
