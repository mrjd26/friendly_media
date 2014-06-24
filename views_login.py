from django.contrib.auth import authenticate, login, logout
from forms import login_form,create_form
from django.shortcuts import redirect,render,render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

def login_screen(request):

    message=''

    if request.method=='POST':
        form=login_form(request.POST)
	
	if form.is_valid():
	    username=request.POST['username']
	    password= request.POST['password']
	    
	    user = authenticate(username=username,password=password)
	    
	    if user is not None:
		if user.is_active:
	            login(request,user)
		    return redirect('/')
		else:
		    message='return a disabled account'	    
		    #return a 'disabled account' error message
	    else:
		message='Email or Password incorrect'
		#return an invalid login error message.
    else:
	form = login_form()

    return render(request,'login.html',{'form':form,'message':message})


def create(request):

	if request.method == 'POST':
		form = create_form(request.POST)

		if form.is_valid():
			password=request.POST['password']
			username=request.POST['username']
			email=request.POST['email']
			User.objects.create_user(username,email,password)
	
			request.session['email'] = email
			message = 'New user '+username+' @ '+email +' created!'

			return redirect(login_screen)

	else:
		form = create_form()

	return render(request,'create.html',{'form':form})

def thanks(request):

	email = request.session['email']
	return render_to_response('thanks.html',{'email':email})

def logout_view(request):
	logout(request)
	return redirect(login_screen)
