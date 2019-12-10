from django.shortcuts import render
# Create your views here.
from .forms import LoginForm, SigninForm
from .models import User

def index(request):
    if request.method == 'GET':
        loginform = LoginForm()
        signinform = SigninForm()
        return render(request, 'index.html', {'loginform' : loginform, 'signinform' : signinform})
    elif request.method == 'POST':
        print(request.POST)
        return render(request, 'index.html')
