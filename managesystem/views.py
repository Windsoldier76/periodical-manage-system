from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.contrib import messages
from .forms import LoginForm, SigninForm
from .models import User, Periodical, PeriodicalIndex

def index(request):
    if request.method == 'GET':
        login_form = LoginForm()
        signin_form = SigninForm()
        return render(request, 'index.html', {'login_form': login_form, 'signin_form': signin_form})
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        signin_form = SigninForm(request.POST)
        '''print(login_form.is_valid())
        print(signin_form.is_valid())
        print("login:", login_form.cleaned_data)
        print("signin", signin_form.cleaned_data)'''
        if login_form.is_valid():
            user_name = login_form.cleaned_data['user_name']
            user_password = login_form.cleaned_data['user_password']
            if User.objects.filter(user_name=user_name).exists():
                user = User.objects.get(user_name=user_name)
                true_password = user.user_password
                if true_password == user_password:
                    isadmin = user.isadmin
                    if isadmin:
                        return redirect('admin_main')#TODO: change admin.html
                    else:
                        return redirect('userPage')
                else:
                    pass
                    # TODO:messages.info(request, '密码错误!')
            else:
                pass
                # TODO:messages.info(request, '无此用户!')

            return render(request, 'index.html', {'login_form': login_form, 'sign_inform': signin_form})


        elif signin_form.is_valid():
            user_name = signin_form.cleaned_data['user_name']
            user_email = signin_form.cleaned_data['user_email']
            user_password = signin_form.cleaned_data['user_password']

            if User.objects.filter(user_name=user_name).exists():
                pass
                # TODO:messages.info(request, '用户名已被占用！')
            else:
                #try:
                print(user_name)
                print(user_password)
                print(user_email)
                User.objects.create(user_name = user_name, user_email = user_email, user_password = user_password)
                User.save()
                    # TODO:messages.info(request, '注册成功！')
                #except:
                 #   pass
                    # TODO:messages.info(request, '注册失败！')
            return render(request, 'index.html', {'login_form': login_form, 'sign_inform': signin_form})

def userPage(request):
    if request.method == 'GET':
        periodical = Periodical.object.all()
        periodicalIndex = PeriodicalIndex.object.all()
        perioList = periodical | periodicalIndex
        return render(request, 'user_main.html', {'perioList': perioList})

