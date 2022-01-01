from django import forms
from django.forms import fields
from django.forms.widgets import Textarea

from blog.models import Comment

class CommentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'class': 'wrap-input'}))
    email = forms.EmailField(
        max_length=245, widget=forms.TextInput(attrs={'class': 'wrap-input'}))
    content_commnet = forms.CharField( widget=forms.Textarea(attrs={'class': 'wrap-input'}))

    class Meta:
        model = Comment
        fields = ['name', 'email', 'content_commnet']
