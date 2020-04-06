from django import forms
from .models import Author

class SignUpForm(forms.Form):
	username = forms.CharField(min_length=3, max_length=60, label="Username", widget=forms.TextInput(attrs={"id":"cName", "class":"full-width", "placeholder":"Type Username"}))
	email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"id":"cEmail", "class":"full-width", "placeholder":"Type Email"}))
	password1 = forms.CharField(min_length=6, label="Password", widget=forms.PasswordInput(attrs={"id":"cWebsite", "class":"full-width", "placeholder":"Type Password"}))
	password2 = forms.CharField(min_length=6, label="Confirm Password", widget=forms.PasswordInput(attrs={"id":"cWebsite", "class":"full-width", "placeholder":"Confirm Password"}))

class LogInForm(forms.Form):
	username = forms.CharField(min_length=3, max_length=60, label="Username", widget=forms.TextInput(attrs={"id":"cName", "class":"full-width", "placeholder":"Type Username"}))
	password = forms.CharField(min_length=6, label="Password", widget=forms.PasswordInput(attrs={"id":"cWebsite", "class":"full-width", "placeholder":"Type Password"}))

class ProfileUpdate(forms.Form):
	pic = forms.FileField(label="Profile Picture", required=False)