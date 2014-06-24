import uuid
from requests import Request
from credentials.models import FacebookCredentials
from django.contrib import messages
from django.shortcuts import render, redirect,render_to_response
from django.contrib.auth.decorators import login_required




@login_required
def facebook_connect(request):
	c = FacebookCredentials()
	state = uuid.uuid4().get_hex()
	request.session['facebook_auth_state'] = state
	params = {
		'client_id':c.FACEBOOK_APP_ID,
		'scope':c.FACEBOOK_SCOPE,
		'state':state,
		'redirect_uri':c.FACEBOOK_REDIRECT_URL
		}

	r = Request('GET', url=c.oauth_url,params=params).prepare()
	return redirect(r.url)

@login_required
def facebook_callback(request):
	error = request.GET.get('error')
	if error:
		description = request.GET.get('description')
		messages.add_message(request, messages.ERROR, description)

	state = request.GET.get('state')
	original_state = request.session.get('facebook_auth_state')

	if state != original_state:
		description = "unauthorized authentication action."
		messages.add_message(request, messages.ERROR, description)

	c = FacebookCredentials()
	code = request.GET.get('code')
	if code:
		#return render_to_response('dashboard.html',{'code':code})
		c.get_user_access_token_from_code(code)
		django_id=request.user.id
		stuff=c.extend_token(django_id)
		#messages.add_message(request, messages.INFO,
		#	_('Login to Facebook successful'))

	return redirect('/')

