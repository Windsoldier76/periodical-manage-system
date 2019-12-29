from django import forms
from django.forms import ModelForm
from .models import *


class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class SigninForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    user_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class ChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your Old Password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your New Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Your New Password'}))

'''
class periodicalindexForm(ModelForm):
    class Meta:
        model = PeriodicalIndex
        fields = ['issn', 'name']
'''