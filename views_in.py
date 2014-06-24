import uuid
from requests import Request
from credentials.models import LinkedinCredentials
from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def in_connect(request):
	c = LinkedinCredentials()
	state = uuid.uuid4().get_hex()
	request.session['linked_auth_state']=state
	params = {
		'response_type':'code',
		'client_id':c.LINKEDIN_API_KEY,
		'scope':'rw_company_admin',
		'state':state,
		'redirect_uri':c.LINKEDIN_REDIRECT_URL
	}

	r = Request('GET', url=c.authorization_code,params=params).prepare()
	return redirect(r.url)

@login_required
def in_callback(request):
	error = request.GET.get('error')
	if error:
		description=request.GET.get('error_description')
		messages.add_message(request,messages.ERROR,description)

	state = request.GET.get('state')
	original_state = request.session.get('linked_auth_state')

	if state != original_state:

		description='unauthorized authentication action.'
		messages.add_message(request,messages.ERROR,description)

	c = LinkedinCredentials()
	code = request.GET.get('code')

	if code:
		django_id=request.user.id
		c.request_access_token(code,django_id)

	return redirect('/')
