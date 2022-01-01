from django import forms
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.forms import fields

from .models import Profile

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'wrap-input', 'readonly': 'readonly'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'wrap-input', 'readonly': 'readonly'}))
    first_name = forms.CharField(
        widget=forms.TextInput())
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'wrap-input'}))
    class Meta:
        model=User
        fields = ('username','email','first_name','last_name')

class UpdateImage(forms.ModelForm):
    class Meta:
        model=Profile
        fields =('picture',)