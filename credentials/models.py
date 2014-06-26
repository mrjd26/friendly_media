from django.db import models
import re
import requests
from django.contrib.auth.models import User
import json

FACEBOOK_APP_ID = '716225878444780'
FACEBOOK_API_SECRET = '403766eb2f6a537027d2bd9b3898872b'
FACEBOOK_SCOPE = 'publish_actions,manage_pages'

TWITTER_API_KEY = 'gKRElHWgABW9w6ckHbnwRS1A6'
TWITTER_API_SECRET = 'OIAWUMdn1IKTgYUfEap8u5uOpPpBgSNznOu9MAL1z4McT3i69l'
TWITTER_ACCESS_TOKEN='1293569622-bfN44wC79YCQ8bFtsMZqYiXQ8225BeM1tDOeUPy'
TWITTER_ACCESS_TOKEN_SECRET='uFmAZjj7UY7xHm0gAxiZYJyH7tJdmQsb40GJnT8r3jfuE'

LINKEDIN_API_KEY = '75xy8hrtu86a2p'
LINKEDIN_SECRET_KEY = 'ouxH5GvjYUmPowTt'

GOOGLE_PLUS_CLIENT_ID ='208026266169-o8ke89laho7m89sknet6epbrktb7389e.apps.googleusercontent.com'
GOOGLE_PLUS_CLIENT_SECRET='aYIRXcbxLFxQfllrwEWnJOQ3'

#BASE_URL = 'http://localhost:8080'
BASE_URL = 'https://myproject0922.appspot.com'

class FacebookCredentials(models.Model):
	FACEBOOK_APP_ID = FACEBOOK_APP_ID
	FACEBOOK_API_SECRET = FACEBOOK_API_SECRET
	FACEBOOK_SCOPE = FACEBOOK_SCOPE
	FACEBOOK_REDIRECT_URL = BASE_URL+'/accounts/facebook_callback'

	TOKEN_RE = 'access_token=(?P<access_token>[^&]+)(?:&expires=(?P<expires>.*))?'
	facebook_url = 'https://www.facebook.com'
	graph_url = 'https://graph.facebook.com'
	access_token_url = graph_url + '/oauth/access_token'
	oauth_url = facebook_url + '/dialog/oauth'
	token_debug_url = graph_url + '/debug_token'
	graph_me_call = graph_url + '/me'
	graph_accounts_call = graph_url + '/me/accounts'
	
	django_id = models.CharField(max_length=255, primary_key=True)
	user_id = models.CharField(max_length=256, blank=True, null=True)
	page_id = models.CharField(max_length=256, blank=True, null=True)
	user_access_token = models.CharField(max_length=512, blank=True, null=True)
	token_expires = models.CharField(max_length=256, blank=True, null=True)


	def get_user_access_token_from_code(self,code):
		payload={
			'client_id':self.FACEBOOK_APP_ID,
			'client_secret':self.FACEBOOK_API_SECRET,
			'redirect_uri':self.FACEBOOK_REDIRECT_URL,
			'code':code
		}
		r = requests.get(self.access_token_url,params=payload)
		
		#tipe = type(r)
		#content = r._content
		#headers = r.headers
		#url = r.url
		#history = r.history
		#encoding = r.encoding
		#reason = r.reason
		#cookies = r.cookies
		#request = r.request
		

		#import urllib
		#from google.appengine.api import urlfetch
		#form_data = urllib.urlencode(payload)
		#f = urlfetch.fetch(url=self.access_token_url,
		#		payload=form_data,
		#		method=urlfetch.GET,
		#		)
		
		#r = f.content
		#h = f.headers
		#hm = f.header_msg
		#sc = f.status_code
		#final_url = f.final_url	

		
		data = re.compile(self.TOKEN_RE).match(r.text).groupdict()
		self.user_access_token = data['access_token']
		#self.token_expires = data['expires']

		#self.save()


	def extend_token(self,django_id):

		params = {
			'client_id': self.FACEBOOK_APP_ID,
			'client_secret':self.FACEBOOK_API_SECRET,
			'grant_type':'fb_exchange_token',
			'fb_exchange_token':self.user_access_token
		}

		r = requests.get(self.access_token_url,params=params)
	
		data=re.compile(self.TOKEN_RE).match(r.text).groupdict()
		self.user_access_token=data['access_token']

		self.token_expires = data['expires']

		self.django_id = django_id
#my code		
		params = {'access_token':self.user_access_token}
		response = requests.get(self.graph_me_call,params=params)
		data = json.loads(response.content)

		user_id = data['id']
		self.user_id = user_id
		
		params = {'access_token':self.user_access_token}
		r = requests.get(self.graph_accounts_call,params=params)
		data = json.loads(r.content)
		page_id = data['data'][0]['id']
	
		self.page_id = page_id		

		self.save()


		return "login successful",self.page_id,self.user_id




class TwitterCredentials(models.Model):
	TWITTER_API_KEY = TWITTER_API_KEY
	TWITTER_API_SECRET = TWITTER_API_SECRET
	TWITTER_REDIRECT_URL = BASE_URL+'/accounts/twitter_callback'
	TWITTER_ACCESS_TOKEN = TWITTER_ACCESS_TOKEN
	TWITTER_ACCESS_TOKEN_SECRET = TWITTER_ACCESS_TOKEN_SECRET

	#TOKEN_RE = 'access_token=(?P<access_token>[^&]+)(?:&expires=(?P<expires>.*))?'
	twitter_url = 'https://api.twitter.com'
	request_token = twitter_url + '/oauth/request_token'
	authenticate = twitter_url + '/oauth/authenticate'
	authorize = twitter_url + '/oauth/authorize'
	access_token_url = twitter_url + '/oauth/access_token'
	
	django_id = models.CharField(max_length=255, primary_key=True)
	user_id = models.CharField(max_length=256, blank=True, null=True)
	screen_name = models.CharField(max_length=256, blank=True, null=True)
	oauth_token = models.CharField(max_length=255, blank=True, null=True)
	oauth_token_secret = models.CharField(max_length=255, blank=True, null=True)
	

	def save_token(self,data):
		self.oauth_token = data['oauth_token']
		self.oauth_token_secret=data['oauth_token_secret']
		self.user_id = data['user_id']
		self.screen_name = data['screen_name']
		self.django_id = data['django_id']		

		self.save()

class LinkedinCredentials(models.Model):
	LINKEDIN_API_KEY = LINKEDIN_API_KEY
	LINKEDIN_SECRET_KEY = LINKEDIN_SECRET_KEY
	linkedin_url = 'https://www.linkedin.com'
	LINKEDIN_REDIRECT_URL = BASE_URL + '/accounts/in_callback'

	authorization_code = linkedin_url + '/uas/oauth2/authorization'
	get_access_token = linkedin_url + '/uas/oauth2/accessToken'
	linkedin_api = 'https://api.linkedin.com/v1'

	django_id = models.CharField(max_length=255,primary_key=True)
	access_token = models.CharField(max_length=255,blank=True,null=True)
	expires_in = models.CharField(max_length=255,blank=True,null=True)
	page_id = models.CharField(max_length=255,blank=True,null=True)


	def request_access_token(self,code,django_id):

		params = {
			'grant_type':'authorization_code',
			'code':code,
			'redirect_uri':self.LINKEDIN_REDIRECT_URL,
			'client_id':self.LINKEDIN_API_KEY,
			'client_secret':self.LINKEDIN_SECRET_KEY
		}

		r = requests.get(self.get_access_token,params=params)
		response = r.json()
		self.expires_in = response['expires_in']
		self.access_token = response['access_token']
		#get page_id
		params={'is-company-admin':'true',
			'oauth2_access_token':self.access_token,
			'format':'json'}
		endpoint = self.linkedin_api + '/companies'

		r = requests.get(endpoint,params=params)
		response = r.json()
		self.page_id = response['values'][0]['id']		

		self.django_id = django_id
		self.save()

class GooglePlusCredentials(models.Model):
	GOOGLE_PLUS_CLIENT_ID = GOOGLE_PLUS_CLIENT_ID
	GOOGLE_PLUS_CLIENT_SECRET = GOOGLE_PLUS_CLIENT_SECRET
	google_accounts_url='https://accounts.google.com'
	auth = google_accounts_url + '/o/oauth2/auth'
	GOOGLE_ACCOUNTS = 'https://accounts.google.com'
	get_access_token= GOOGLE_ACCOUNTS  + '/o/oauth2/token'
	GOOGLE_PLUS_REDIRECT_URL = BASE_URL+'/accounts/g_callback'



	django_id = models.CharField(max_length=255,primary_key=True)
	access_token = models.CharField(max_length=255,blank=True,null=True)
	expires_in = models.CharField(max_length=255,blank=True,null=True)
	refresh_token=models.TextField(blank=True,null=True)
	token_type=models.CharField(max_length=255,blank=True,null=True)

	def request_access_token(self,code,django_id):

		params = {
			'grant_type':'authorization_code',
			'code':code,
			'redirect_uri':self.GOOGLE_PLUS_REDIRECT_URL,
			'client_id':self.GOOGLE_PLUS_CLIENT_ID,
			'client_secret':self.GOOGLE_PLUS_CLIENT_SECRET
		}
		r = requests.post(self.get_access_token,data=params)
		response_content=r.content
		response_header=r.headers
		response_reason=r.reason
		response_request=r.request
		response_url=r.url
		response_encoding=r.encoding
		response = r.json()
		self.access_token=response['access_token']
		self.refresh_token=response['id_token']
		self.expires_in=response['expires_in']
		self.token_type=response['token_type']
		self.django_id = django_id
		self.save()





# upload form model

class upload(models.Model):
	image=models.ImageField(upload_to='static')
	text=models.CharField(max_length=255)
	link=models.CharField(max_length=255)
	title=models.CharField(max_length=255)
