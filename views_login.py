from django.contrib.auth import authenticate, login, logout
from forms import login_form,create_form
from django.shortcuts import redirect,render,render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


#imports for '/thanks/' view on successful registration

from google.appengine.api import mail

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
			user_address=request.POST['email']

			#additional verification for valid email address from google
	
			if not mail.is_email_valid(user_address):
				form=create_form()
		
				return render(request,'create.htl',{'form':form})
			
	
			else:
				sender_address="Friendly-Media.com Support <friendlymedia.incorporation@gmail.com>"

				subject="Confirm your registration"

				body = """
Thank you for creating an account! Please confirm your email address by
clicking on the link below:

%s
""" %('https://myproject0922.appspot.com/confirmed?email='+user_address+'&username='+username)				

				mail.send_mail(sender_address,user_address,subject,body)
				#user address == email (for django auth model)
				email=user_address
				User.objects.create_user(username,email,password)
				q = User.objects.filter(username=username,email=email)
				a = q[0]
				a.is_active=False
				a.save()			

				return render_to_response('thanks.html',{'user_address':user_address,'is_active':a.is_active})

	else:
		form = create_form()

	return render(request,'create.html',{'form':form})

def confirmed(request):

	user_address=request.GET['email']
	username=request.GET['username']

	q = User.objects.filter(email=user_address,username=username)	
	
	a = q[0]
	a.is_active=True
	a.save()

	return render_to_response('confirmed.html',{'is_active':a.is_active})

def logout_view(request):
	logout(request)
	return redirect(login_screen)
