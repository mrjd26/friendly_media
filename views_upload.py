from django.shortcuts import render_to_response



def upload(request):
	if request.session['twitter_state']:
		tw_png_source = '/static/check.png'

	else:
		tw_png_source = '/static/yield.png'

	if request.session['facebook_state']:
		fb_png_source = '/static/check.png'
	else:
		fb_png_source = '/static/yield.png'

	if request.session['linkedin_state']:
		in_png_source = '/static/check.png'
	else:
		in_png_source = '/static/yield.png'
	if request.session['gplus_state']:
		gplus_png_source = '/static/check.png'
	else:
		gplus_png_source = '/static/yield.png'




	return render_to_response('upload.html',{'tw_png_source':tw_png_source,'fb_png_source':fb_png_source,'in_png_source':in_png_source,'gplus_png_source':gplus_png_source})
