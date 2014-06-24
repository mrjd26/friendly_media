from django import forms


class login_form(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)

class create_form(forms.Form):
	
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)
	email = forms.EmailField()
