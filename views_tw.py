import requests
from requests import Request
from credentials.models import TwitterCredentials
from django.contrib import messages
from django.shortcuts import render, redirect,render_to_response
from django.contrib.auth.decorators import login_required
import re
import uuid
import time
from requests_oauthlib import OAuth1

@login_required
def twitter_connect(request):
	
	TOKEN_RE='oauth_token=(?P<oauth_token>[^&]+)(?:&oauth_token_secret=(?P<oauth_token_secret>[^&]+))(?:&oauth_callback_confirmed=(?P<oauth_callback_cofirmed>.*))?'

	nonce = uuid.uuid4().get_hex()
	timestamp = time.time()

	c = TwitterCredentials()

	oauth = OAuth1(c.TWITTER_API_KEY,client_secret=c.TWITTER_API_SECRET,callback_uri=c.TWITTER_REDIRECT_URL)

	r = requests.post(c.request_token,auth=oauth)
	data = re.compile(TOKEN_RE).match(r.text).groupdict()
	a=r.content
	b=r.headers
	d=r.history
	e=r.reason
	f=r.request
	g=r.encoding

	params = {'oauth_token':data['oauth_token']}

	request.session['oauth_token_secret'] = data['oauth_token_secret']

	r = Request('GET',url=c.authorize,params=params).prepare()
	return redirect(r.url)

	#return render_to_response('dashboard.html',{'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'g':data})

@login_required
def twitter_callback(request):
	
	oauth_token = request.GET.get('oauth_token')
	oauth_verifier = request.GET.get('oauth_verifier')
	oauth_token_secret = request.session['oauth_token_secret']
	
	c = TwitterCredentials()

	oauth = OAuth1(c.TWITTER_API_KEY,
			client_secret=c.TWITTER_API_SECRET,
			resource_owner_key=oauth_token,
			resource_owner_secret=oauth_token_secret,
			verifier=oauth_verifier)

	r = requests.post(url=c.access_token_url,auth=oauth)

	
	TOKEN_RE='oauth_token=(?P<oauth_token>[^&]+)(?:&oauth_token_secret=(?P<oauth_token_secret>[^&]+))(?:&user_id=(?P<user_id>[^&]+))(?:&screen_name=(?P<screen_name>.*))?'

	
	data = re.compile(TOKEN_RE).match(r.text).groupdict()
	
	data['django_id'] = request.user.id

	c.save_token(data)

	a=r.content
	b=r.headers
	c=r.url
	d=r.history
	e=r.reason
	f=r.request
	g=r.encoding

	return redirect('/')

