
from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse
import json
from calls import Twitter
from credentials.models import TwitterCredentials


def ajax_call(request):

	session_id=request.user.id

	try:
                o = TwitterCredentials.objects.get(django_id=session_id)
        except:
                pass

        if o:
                user_id = o.user_id
                screen_name = o.screen_name
                oauth_token = o.oauth_token
                oauth_token_secret = o.oauth_token_secret
                TWITTER_API_KEY = o.TWITTER_API_KEY
                TWITTER_API_SECRET = o.TWITTER_API_SECRET

                T = Twitter(session_id,TWITTER_API_KEY,TWITTER_API_SECRET,oauth_token,oauth_token_secret)



	id_string=request.GET["identifier"]

	#endpoint = "/statuses/show.json?id="+id_string
	
	endpoint ="/favorites/create.json"
	params={"id":id_string} 

	data = T.api_call_post(endpoint,params)

	return HttpResponse(json.dumps(data))
	
