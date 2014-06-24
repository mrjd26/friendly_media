import uuid
from requests import Request
from django.shortcuts import render, redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from credentials.models import GooglePlusCredentials

@login_required
def g_connect(request):
	g = GooglePlusCredentials()
	state = uuid.uuid4().get_hex()
	request.session['g_auth_state']=state
	params = {
		'scope':'https://www.googleapis.com/auth/plus.login',
		'state':state,
		'redirect_uri':'https://myproject0922.appspot.com/accounts/g_callback',
		'response_type':'code',
		'client_id':g.GOOGLE_PLUS_CLIENT_ID,
		'access_type':'offline'
	}
	
	r = Request('GET', url=g.auth,params=params).prepare()
	return redirect(r.url)

@login_required
def g_callback(request):
	state = request.GET.get('state')
	original_state = request.session.get('g_auth_state')

	if state!= original_state:
		description='unauthorized authentication action'
		messages.add_message(request,description)
	code = request.GET.get('code')

	if code:

		g = GooglePlusCredentials()
		django_id = request.user.id
		g.request_access_token(code,django_id)

	return redirect('/')
