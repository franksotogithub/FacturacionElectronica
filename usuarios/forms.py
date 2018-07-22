from django import forms
from .models import Usuario



class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Usuario'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))


