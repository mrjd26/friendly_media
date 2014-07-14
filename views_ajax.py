
from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse
import json

def ajax_call(request):

	data = {}
	
	data["foo"] = "bar"

	return HttpResponse(json.dumps(data))
