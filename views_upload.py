from django.shortcuts import render_to_response
from forms import uploadform
from credentials.models import upload



def upload(request):

	user = request.user.id

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
			new_post.save()
	
			return HttpResponseRedirect('/')

	else:
		form = uploadform()

	return render_to_response('upload.html',{'form':form,'tw_png_source':tw_png_source,'fb_png_source':fb_png_source,'in_png_source':in_png_source,'gplus_png_source':gplus_png_source,'tw_state':tw_state,'fb_state':fb_state,'in_state':in_state,'g_state':g_state})
