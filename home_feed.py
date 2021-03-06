
import requests
from dateutil import parser
from datetime import datetime

graph_url = 'https://graph.facebook.com'

def order_feed(all_feeds):

	for post in all_feeds:
	#created_time key
		#twitter-time
		if 'created_at' in post:
			post['created_time'] = post.pop('created_at')

			

		#message key
		if 'text' in post:	
			post['message'] = post.pop('text')
		#twitter picture to link key
		if 'entities' in post:
			if 'media' in post['entities']:
				post['link']=post['entities']['media'][0]['media_url']		

		#assign datetime.datetime
		#post['created_time'] = parser.parse(post['created_time'])
		#twitter profile pic
		if 'user' in post:
			post['profile_pic'] = post['user']['profile_image_url']
			post['name']=post['user']['name']
			post['platform']='twitter'
				
			post['created_time'] = parser.parse(post['created_time'])
			post["id"]=str(post["id"])
		#facebook profile pic from graph call in views.py
		if 'from' in post:
			poster_id=post['from']['id']
			endpoint=graph_url+'/'+poster_id+'/picture'
			params={'redirect':'false'}
			r=requests.get(endpoint,params=params)
			data=r.json()
			profile_pic=data['data']['url']
			post['profile_pic']=profile_pic

			post['name']=post['from']['name']
			post['platform']='facebook'
			
			post['created_time'] = parser.parse(post['created_time'])

			if 'picture' in post:
				ndx_of_s = post['picture'].rfind('s')
				ndx_of_n = post['picture'].rfind('n')
				if ndx_of_s > 50:
					new_link = post['picture'][:ndx_of_s]+'n'+post['picture'][ndx_of_s+1:]
				else:
					new_link=post['picture']
				post['picture']=new_link


			if 'source' in post:
				link=post['source']
				ndx=link.find('p')
				link=link[:ndx+1]+'s'+link[ndx+1:]
				link=link.strip("&autoplay=1")
				post["source"]=link

		#linkedin-time
		if 'timestamp' in post:
			timestamp = post['timestamp']
			stringify = str(timestamp)
			in_sec = stringify[0:-3]
			floated = float(in_sec)
			obj = datetime.fromtimestamp(floated)
			strftime = datetime.strftime(obj,'%Y %d %b %H:%M:%S +0000')
			
			post['created_time']=parser.parse(strftime)
			post['platform']='linkedin'
			
	return all_feeds
