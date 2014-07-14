import uuid
from requests import Request
from credentials.models import InstagramCredentials
from django.contrib import messages
from django.shortcuts import render, redirect,render_to_response
from django.contrib.auth.decorators import login_required




@login_required
def instagram_connect(request):
        c = InstagramCredentials()
        state = uuid.uuid4().get_hex()
        request.session['instagram_auth_state'] = state
        params = {
                'client_id':c.INSTAGRAM_CLIENT_ID,
                'response_type':"code",
		"scope":"likes comments relationships basic",
                'state':state,
                'redirect_uri':c.INSTAGRAM_REDIRECT_URI
                }

        r = Request('GET', url=c.authorize,params=params).prepare()
        return redirect(r.url)

@login_required
def instagram_callback(request):
        error = request.GET.get('error')
        if error:
                description = request.GET.get('description')
                messages.add_message(request, messages.ERROR, description)

        state = request.GET.get('state')
        original_state = request.session.get('instagram_auth_state')

        if state != original_state:
                description = "unauthorized authentication action."
                messages.add_message(request, messages.ERROR, description)

        c = InstagramCredentials()
        code = request.GET.get('code')
        if code:
                c.get_access_token(code)
                django_id=request.user.id
        return redirect('/')

