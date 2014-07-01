from requests_oauthlib import OAuth1
import requests
import json

graph_url = 'https://graph.facebook.com'
twitter_api_url = 'https://api.twitter.com/1.1'
linkedin_url = 'https://api.linkedin.com/v1'

class Facebook:

	def __init__(self,django_id):

		self.django_id = django_id

	def api_call(self,endpoint,params):

		page_feed_endpoint = graph_url + endpoint
		r = requests.get(page_feed_endpoint,params=params)
		
		fb_feed = r.json()

		return fb_feed
	def api_call_post(self,endpoint,params):
		page_feed_endpoint = graph_url + endpoint
		r = requests.post(page_feed_endpoint,params=params)
		
		return r.content,r.reason

class Twitter:

	def __init__(self,django_id,TWITTER_API_KEY,TWITTER_API_SECRET,oauth_token,oauth_token_secret):

		self.django_id = django_id
		self.TWITTER_API_KEY = TWITTER_API_KEY
		self.TWITTER_API_SECRET = TWITTER_API_SECRET
		self.oauth_token = oauth_token
		self.oauth_token_secret = oauth_token_secret

	def api_call(self,endpoint):

		oauth = OAuth1(self.TWITTER_API_KEY,
		client_secret=self.TWITTER_API_SECRET,
		resource_owner_key=self.oauth_token,
		resource_owner_secret=self.oauth_token_secret)
		user_timeline_url = twitter_api_url + endpoint
		r = requests.get(user_timeline_url,auth=oauth)
		tw_feed = r.json()
		
		return tw_feed

	def api_call_post(self,endpoint,params):
		call_endpoint = twitter_api_url + endpoint

		oauth = OAuth1(self.TWITTER_API_KEY,
		client_secret=self.TWITTER_API_SECRET,
		resource_owner_key=self.oauth_token,
		resource_owner_secret=self.oauth_token_secret)

		headers = {'Content-Type':'application/octet-stream'}		

		r = requests.request('POST',call_endpoint,auth=oauth,headers=headers,params=params)

		return r.content,r.reason,r.url

class Linkedin:
	
	def __init__(self,django_id):
	
		self.django_id = django_id

	def api_call(self,endpoint,params):

		call_endpoint = linkedin_url + endpoint
		r = requests.get(call_endpoint,params=params)
		in_read = r.json()
		
		#linkedin list
		try:
			in_read = in_read['values']
		except:
			in_read = []
		return in_read

	def api_call_post(self,endpoint,params,data,headers):
		call_endpoint = linkedin_url + endpoint
		r = requests.request('POST',call_endpoint,data=json.dumps(data),params=params,headers=headers)
		return r.content,r.url,r.headers

	def api_call_company(self,endpoint,params):
		call_endpoint = linkedin_url + endpoint
		r = requests.get(call_endpoint,params=params)
		company = r.json()
		return company	
