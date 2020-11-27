from django import forms
from django.contrib.auth.models import User

from . models import Vine,VineAlbum


class VineAlbum_form(forms.ModelForm):

    class Meta:
        model = VineAlbum
        fields = ['artist', 'title', 'genre', 'vine_logo']


class Vine_form(forms.ModelForm):

    class Meta:
        model = Vine
        fields = ['vine_title','language','country','vine_poster','video']

class UserForm(forms.ModelForm):
    about_me= forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 26}))
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password','about_me']


class Login(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    model = User
    fields = ['username', 'password']