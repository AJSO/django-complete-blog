from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'firstname','class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'lastname','class':'form-control'})) 
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder':'username','class':'form-control'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'email','class':'form-control'}))
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'address','class':'form-control'}))
    
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','address', 'email', 'password1', 'password2')

