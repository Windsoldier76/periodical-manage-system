from django.shortcuts import render
# Create your views here.
from django.contrib import messages
from .forms import LoginForm, SigninForm
from .models import User

def index(request):
    if request.method == 'GET':
        loginform = LoginForm()
        signinform = SigninForm()
        return render(request, 'index.html', {'loginform' : loginform, 'signinform' : signinform})
    elif request.method == 'POST':
        loginform = LoginForm(request.POST or None)
        signinform = SigninForm(request.POST or None)
        print(request.POST)
        print(loginform.is_valid())
        if loginform.is_valid():
            print("post success")
            try:
                print(loginform)
                username = User.objects.get(user_name = 'user_name')
                isadmin = User.objects.get(user_name = 'user_name').value('isadmin')
                print(isadmin)
                if isadmin:
                    pass# TODO: add a view link
                else:
                    return render(request, 'user_main.html')
            except:
                messages.info(request, '无此用户!')


        elif signinform.is_valid():
            user = User.objects.get(user_name = 'user_name')
            if user:
                messages.info(request, '用户名已被占用！')
            else:
                try:
                    newuser = User.objects.create(user_name = 'user_name', user_email = 'user_email', user_password = 'user_password')
                    messages.info(request, '注册成功！')
                except:
                    messages.info(request, '注册失败！')
        return render(request, 'index.html', {'loginform' : loginform, 'signinform' : signinform})



