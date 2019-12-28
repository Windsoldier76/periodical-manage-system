from django.shortcuts import render
from django.shortcuts import redirect
from managesystem import models
# Create your views here.
from django.contrib import messages
from .forms import LoginForm, SigninForm
from .models import User, Periodical, PeriodicalIndex
from .models import PeriodicalInfo, Borrow, Purchase
import datetime

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
                        return redirect('userPage', user_name=user_name)
                else:
                    pass
                    # TODO:messages.info(request, '密码错误!')
            else:
                pass
                # TODO:messages.info(request, '无此用户!')

            return redirect('index')


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
            return redirect('index')

def userPage(request, user_name):
    if request.method == 'GET':
        periodical = Periodical.objects.all()
        periodicalIndex = PeriodicalIndex.objects.all()
        # showList = Periodical.objects.filter(id=id)
        # showList = periodical.PeriodicalIndex_set.all()
        return render(request, 'login/user_main.html', {'perioindexList': periodicalIndex,
                                                        'perioList': periodical,
                                                        'username': user_name})
        # return render(request, 'login/user_main.html', {'showList': showList})

def borrowBook(request, user_name, book_id):
    periodical = Periodical.objects.get(id=book_id)
    username = User.objects.get(user_name=user_name)

    Borrow.objects.create(user_name=username, book_id=periodical)

    periodical.residue -= 1
    periodical.save()

    return redirect('userPage', user_name=user_name)

def borrowShow(request, user_name):
    borrowList = Borrow.objects.filter(user_name=user_name)
    periodical = Periodical.objects.all()
    periodicalIndex = PeriodicalIndex.objects.all()
    return render(request, 'login/hasborrow.html', {'borrowList': borrowList,
                                                    'perioindexList': periodicalIndex,
                                                    'perioList': periodical,
                                                    'username': user_name})

def backBook(request, user_name, borrow_id):


    borrow = Borrow.objects.get(id=borrow_id)
    periodical = id=borrow.book_id

    borrow.back_date = datetime.datetime.now()
    borrow.save()

    periodical.residue += 1
    periodical.save()
    print("归还成功")
    return redirect('borrowShow', user_name=user_name)