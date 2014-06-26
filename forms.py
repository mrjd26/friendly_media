from django import forms
from credentials.models import upload

class login_form(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)

class create_form(forms.Form):
	
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)
	email = forms.EmailField()



class uploadform(forms.ModelForm):
	class Meta:
		model = upload
		field = ('image','text','link','title')
		
		widgets={'text':forms.Textarea(attrs={'cols':80,'rows':2})}
		
