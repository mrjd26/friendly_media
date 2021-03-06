from django.shortcuts import render,render_to_response
from forms import uploadform
from credentials.models import upload,FacebookCredentials,LinkedinCredentials,TwitterCredentials,GooglePlusCredentials
from django.http import HttpResponseRedirect
from calls import Facebook,Linkedin,Twitter,Google
from django.contrib.auth.decorators import login_required
#google cloud services imports
from google.appengine.api import app_identity
import cloudstorage as gcs
from google.appengine.ext import blobstore
from google.appengine.api.images import get_serving_url


import os
import json

from twython import Twython
from StringIO import StringIO

output = []
bucket_name = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())

output.append(bucket_name)


@login_required
def upload(request):

	
	if request.session['twitter_state']:
		tw_png_source = '/static/check.png'
		tw_state = 'checked'

	else:
		tw_png_source = '/static/yield.png'
		tw_state = 'disabled'

	if request.session['facebook_state']:
		fb_png_source = '/static/check.png'
		fb_state = 'checked'
	else:
		fb_png_source = '/static/yield.png'
		fb_state = 'disabled'

	if request.session['linkedin_state']:
		in_png_source = '/static/check.png'
		in_state = 'checked'
	else:
		in_png_source = '/static/yield.png'
		in_state='disabled'

	if request.session['gplus_state']:
		gplus_png_source = '/static/check.png'
		g_state = 'checked'
	else:
		gplus_png_source = '/static/yield.png'
		g_state='disabled'


	if request.method=='POST':
	
		form = uploadform(request.POST,request.FILES)

		if form.is_valid():
			new_post = form.save(commit=False)
			#new_post.save()
	
			return HttpResponseRedirect('/upload_process/')

	else:
		form = uploadform()

	return render(request,'upload.html',{'form':form,'tw_png_source':tw_png_source,'fb_png_source':fb_png_source,'in_png_source':in_png_source,'gplus_png_source':gplus_png_source,'tw_state':tw_state,'fb_state':fb_state,'in_state':in_state,'g_state':g_state})
@login_required
def upload_process(request):
	
	user = request.user.id

	if 'text' in request.POST:
		text = request.POST['text']
	if 'link' in request.POST:
		link = request.POST['link']
	
	if 'title' in request.POST:
		title= request.POST['title']
	if 'image' in request.FILES and request.FILES['image']:

		#django methods for ImageField
		content_type = request.FILES['image'].content_type
		name = request.FILES['image'].name
		
		# file upload to google cloud storage 
		# for easy URL serving

		# q = upload(image=name)
		# q.save()

		upload_file = request.FILES['image']
		data = upload_file.read()
		gcs_file = gcs.open(('/'+bucket_name + '/' + name),mode='w',content_type=content_type,options={'x-goog-acl':'bucket-owner-full-control'})
		gcs_file.write(data)
		gcs_file.close()

	#after writing to gcs, get_serving_url
	
		picture = gcs.open('/'+bucket_name+'/'+name)
		blob_key=blobstore.create_gs_key('/gs/'+bucket_name+'/'+name)
		serving_url=get_serving_url(blob_key)
		stats=gcs.stat('/'+bucket_name+'/'+name)
	else:
		name=""	
		serving_url=""

	if 'platform' in request.POST:
        	platform = request.POST.getlist('platform')

	if 'facebook' in platform:
		p = FacebookCredentials.objects.get(django_id=user)
		page_id = p.page_id
		page_access_token = p.page_access_token
		
		#call API
		if 'image' in request.FILES and request.FILES['image']:
			F = Facebook(user)
			
			endpoint='/' + page_id + '/photos'
			params={'access_token':page_access_token,
				'url':serving_url,
				'message':text,
				}

			data1,data2=F.api_call_post(endpoint,params)

		else:
			F = Facebook(user)

			endpoint='/'+page_id+'/feed'
			params={'access_token':page_access_token,
				'message':text,
				'link':link,}
			data1,data2 = F.api_call_post(endpoint,params)

	if 'linkedin' in platform:

		#'link' field true by default
		is_a_link = True	

		k = LinkedinCredentials.objects.get(django_id=user)
		page_id = k.page_id
		page_access_token = k.access_token
	
		if len(request.POST['link'])<2:
			link=name

			is_a_link = False

		#call API
		if 'image' in request.FILES and request.FILES['image']:
			L = Linkedin(user)
			
			endpoint = '/' + 'companies/'+page_id+'/shares'
			

			headers={"content-type":"application/json",
				"x-li-format":"json"}

			params={"oauth2_access_token":page_access_token}

			data={
				"visibility":{"code":"anyone"},
				"comment":text,
				"content":{
					"submitted-url":link,
					"title":title,
					"description":text,
					"submitted-image-url":serving_url,
					},
				}
			data1,data2,data3=L.api_call_post(endpoint,params,data,headers)

		elif is_a_link == True:
			
			L = Linkedin(user)
			
			endpoint = '/' + 'companies/'+page_id+'/shares'
			

			headers={"content-type":"application/json",
				"x-li-format":"json"}

			params={"oauth2_access_token":page_access_token}

	
			data={
				"comment":link,
				"visibility":{"code":"anyone"},		
				}

			data1,data2,data3=L.api_call_post(endpoint,params,data,headers)


		else:
			L = Linkedin(user)
			endpoint = '/'+'companies/'+page_id+'/shares'
			headers={"Content-Type":"application/json",
				"x-li-format":"json"}
		
			params={"oauth2_access_token":page_access_token}
	
			data={
				"comment":text,
				"visibility":{"code":"anyone"},		
				}

			data1,data2,data3=L.api_call_post(endpoint,params,data,headers)

	if 'twitter' in platform:
		o = TwitterCredentials.objects.get(django_id=user)
		oauth_token = o.oauth_token
		oauth_token_secret = o.oauth_token_secret
		TWITTER_API_KEY = o.TWITTER_API_KEY
		TWITTER_API_SECRET=o.TWITTER_API_SECRET
			

		if 'image' in request.FILES and request.FILES['image']:
				
			file_object = request.FILES['image']
			file_object.open()
			img=file_object.read()
				
			#Had to go with Twython to get statuses/update_with_media working
	
			twitter=Twython(TWITTER_API_KEY,TWITTER_API_SECRET,oauth_token,oauth_token_secret)
							
			twitter.update_status_with_media(media=StringIO(img),status=(text+' '+link))
	
		else:
			T = Twitter(user,TWITTER_API_KEY,TWITTER_API_SECRET,oauth_token,oauth_token_secret)
			endpoint = '/statuses/update.json'
			params = {'status':(text+' '+link)}
			T.api_call_post(endpoint,params)
				

	if 'gplus' in platform:
			
		k = GooglePlusCredentials.objects.get(django_id=user)
		endpoint='/people/me/moments/vault'
		access_token = k.access_token		

		G=Google(user)

		a,b,c,d=G.api_call_post(endpoint,access_token)
	
	return render_to_response('dashboard.html',{'data1':a,'data2':b,'data3':c,'data4':d})
