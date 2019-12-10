from django.forms import ModelForm, TextInput, PasswordInput
from .models import User


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'user_password']
        widgets = {
            'user_name': TextInput(attrs={'placeholder': 'Username'}),
            'user_password': PasswordInput(attrs={'placeholder': 'Password'})
        }


class SigninForm(ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'user_email', 'user_password']
        widgets = {
            'user_name': TextInput(attrs={'placeholder': 'Username'}),
            'user_email':TextInput(attrs={'placeholder': 'Email'}),
            'user_password': PasswordInput(attrs={'placeholder': 'Password'})
        }