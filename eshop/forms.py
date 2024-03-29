from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    name=forms.CharField(max_length=50)
    phone=forms.CharField(max_length=10)
    email=forms.EmailField()
    address=forms.CharField(widget=forms.Textarea)
    class Meta:
        model = User
        fields = ('username','password1','password2','name','phone','email','address')

class UpdateForm(forms.ModelForm):
    phone=forms.CharField(max_length=10)
    email=forms.EmailField()
    address=forms.CharField(widget=forms.Textarea)
    class Meta:
        model = User
        fields = ('phone','email','address')