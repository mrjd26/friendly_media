from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

@csrf_exempt
@xframe_options_exempt
def custom_tab(request):
	


	return render_to_response("custom_tab.html",{})
