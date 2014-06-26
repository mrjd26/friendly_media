from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from credentials.models import FacebookCredentials,TwitterCredentials,LinkedinCredentials,GooglePlusCredentials
from calls import Facebook,Twitter,Linkedin
from home_feed import order_feed


@login_required
def dashboard(request):
	session_id  = request.user.id
	p = False
	o = False
	L = False
	k = False
#fbfeed 
#see if FB credentials in Model

	try:
		p = FacebookCredentials.objects.get(django_id=session_id)
	except:
		pass	
	if p:
		user_id = p.user_id
		page_id = p.page_id
		user_access_token = p.user_access_token
		fb_png_source = '/static/check.png'
		
		#call API
		F = Facebook(session_id)
		
		#page feed
		endpoint='/'+page_id+'/feed'
		params={'access_token':user_access_token}
		fb_feed = F.api_call(endpoint,params)
		fb_feed = fb_feed['data']
		
		#set session for FB state
		request.session['facebook_state']=True
		
	else:
		fb_png_source = '/static/yield.png'	
		user_id = None
		fb_feed = []
		
		#set session for FB state
	
		request.session['facebook_state']=False


#Linkedin
#is user Linked in !!??

	try:
		L = LinkedinCredentials.objects.get(django_id=session_id)
	except:
		pass
	if L:
		in_png_source='/static/check.png'
		access_token=L.access_token		

		page_id = L.page_id

		#call API
		I = Linkedin(session_id)

		#company
		endpoint = '/companies/'+page_id+'/updates/'
		params={'oauth2_access_token':access_token,
			'format':'json'}
		in_read = I.api_call(endpoint,params)

		#set session for linkedin state

		request.session['linkedin_state']=True	
	else:
		in_png_source='/static/yield.png'
		in_read =[]
		
		request.session['linkedin_state']=False
		
#tweets
#see if TW credentials in Model

	try:
		o = TwitterCredentials.objects.get(django_id=session_id)
	except:
		pass

	if o:
		user_id = o.user_id
		screen_name = o.screen_name
		oauth_token = o.oauth_token
		oauth_token_secret = o.oauth_token_secret
		tw_png_source = '/static/check.png'
		
		TWITTER_API_KEY = o.TWITTER_API_KEY
		TWITTER_API_SECRET = o.TWITTER_API_SECRET

		#call API
		T = Twitter(session_id,TWITTER_API_KEY,TWITTER_API_SECRET,oauth_token,oauth_token_secret)

		#user timeline
		endpoint = '/statuses/user_timeline.json'
		tw_feed = T.api_call(endpoint)
		#mentions_timeline
		endpoint = '/statuses/mentions_timeline.json'
		tw_mentions = T.api_call(endpoint)		
		#retweets_of_me
		endpoint = '/statuses/retweets_of_me.json'
		tw_retweets = T.api_call(endpoint)

		#set session of Twitter state
		request.session['twitter_state']=True

		
	else:
		tw_png_source = '/static/yield.png'
		user_id=None
		tw_feed = []
		tw_mentions=[]
		tw_retweets=[]
		
		#set session of Twitter state
		request.session['twitter_state']=False

#gplus connection

	try:
		k = GooglePlusCredentials.objects.get(django_id=session_id)
	except:
		pass

	if k:
		#call api 
		gplus_png_source='/static/check.png'
		gplus='gplus api call'

		#set sessions of gplus state
		request.session['gplus_state']=True
	else:
		gplus_png_source='/static/yield.png'
		gplus = []

		#set session of gplus state
		request.session['gplus_state']=False
	

	all_feeds = fb_feed + tw_feed + tw_mentions + tw_retweets + in_read

	home_feed = order_feed(all_feeds)

	return render(request,'dashboard.html',{'fb_png_source':fb_png_source,'tw_png_source':tw_png_source,'in_png_source':in_png_source,'gplus_png_source':gplus_png_source,'home_feed':home_feed})

