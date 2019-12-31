from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib import messages
from managesystem import models
# Create your views here.
from django.contrib import messages
from .forms import LoginForm, SigninForm
from .forms import ChangeForm
from .models import User, Periodical, PeriodicalIndex
from .models import PeriodicalInfo, Borrow, Purchase
import datetime


def index(request):
    # 登录界面
    if request.method == 'GET':
        # 当request请求为get时
        login_form = LoginForm()
        signin_form = SigninForm()
        return render(request, 'index.html', {'login_form': login_form, 'signin_form': signin_form})
    elif request.method == 'POST':
        # 当request请求为post时
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        user_password = request.POST.get('user_password')

        if not user_email:
            # 请求登录
            if User.objects.filter(user_name=user_name).exists():
                #验证用户名
                user = User.objects.get(user_name=user_name)
                true_password = user.user_password
                if true_password == user_password:
                    # 验证密码
                    isadmin = user.isadmin
                    if isadmin:
                        # 验证管理员身份
                        return redirect('adminPage', user_name=user_name)#TODO: change admin.html
                    else:
                        return redirect('userPage', user_name=user_name)
                else:
                    print("密码错误！")
                    messages.info(request, '密码错误!')
            else:
                messages.info(request, '无此用户!')

            return redirect('index')

        else:
            # 请求注册
            if User.objects.filter(user_name=user_name).exists():
                # 验证重名
                messages.info(request, '用户名已被占用！')
            else:
                try:
                    print(User)
                    print(user_email)
                    User.objects.create(user_name = user_name, user_email = user_email, user_password = user_password)
                    messages.info(request, '注册成功！')
                except:
                    messages.info(request, '注册失败！')
            return redirect('index')


def userPage(request, user_name):
    # 用户界面
    if request.method == 'GET':
        change_form = ChangeForm()
        searchword = request.GET.get('search')
        if searchword:
            searchflag = request.GET.get('optionsRadios')
            if searchflag == "option1":
                # 书名查询
                periodical = Periodical.objects.all()
                periodicalIndex = PeriodicalIndex.objects.filter(name=searchword)
            elif searchflag == "option2":
                # 书籍编号查询
                periodical = Periodical.objects.filter(id=searchword)
                periodicalIndex = PeriodicalIndex.objects.all()
            elif searchflag == "option3":
                # 文章关键字查询
                periodical = Periodical.objects.filter(Q(periodicalinfo__first_author=searchword)|
                                                       Q(periodicalinfo__second_author=searchword)|
                                                       Q(periodicalinfo__third_author=searchword)|
                                                       Q(periodicalinfo__forth_author=searchword)|
                                                       Q(periodicalinfo__first_keyword=searchword)|
                                                       Q(periodicalinfo__second_keyword=searchword)|
                                                       Q(periodicalinfo__third_keyword=searchword)|
                                                       Q(periodicalinfo__forth_keyword=searchword)|
                                                       Q(periodicalinfo__fifth_keyword=searchword)|
                                                       Q(periodicalinfo__paper_name=searchword))
                periodicalIndex = PeriodicalIndex.objects.all()
        else:
            periodical = Periodical.objects.all()
            periodicalIndex = PeriodicalIndex.objects.all()

        return render(request, 'login/user_main.html', {'perioindexList': periodicalIndex,
                                                        'perioList': periodical,
                                                        'username': user_name,
                                                        'ChangeForm': change_form})
    elif request.method == 'POST':
        change_form = ChangeForm(request.POST)
        if change_form.is_valid():
            old_password = change_form.cleaned_data['old_password']
            new_password = change_form.cleaned_data['new_password']
            confirm_password = change_form.cleaned_data['confirm_password']

            user = User.objects.get(user_name=user_name)
            if old_password == user.user_password:
                if new_password == confirm_password:
                    user.user_password = new_password
                    user.save()
                    messages.info(request, '修改成功！')
                else:
                    messages.info(request, '两次输入密码不一致！')
            else:
                messages.info(request, '旧密码输入错误！')

        return redirect('userPage', user_name=user_name)

def perioInfo(request, user_name, book_id):
    # 期刊信息
    user = User.objects.get(user_name=user_name)
    if request.method == 'GET':
        change_form = ChangeForm()
        periodical = Periodical.objects.get(id=book_id)
        articleList = PeriodicalInfo.objects.filter(book_id=periodical)
        isadmin = user.isadmin
        return render(request, 'login/perioinfo.html', {'articleList': articleList,
                                                        'username':user_name,
                                                        'ChangeForm': change_form,
                                                        'isadmin':isadmin})
    elif request.method == 'POST':
        change_form = ChangeForm(request.POST)
        if change_form.is_valid():
            old_password = change_form.cleaned_data['old_password']
            new_password = change_form.cleaned_data['new_password']
            confirm_password = change_form.cleaned_data['confirm_password']

            if old_password == user.user_password:
                if new_password == confirm_password:
                    user.user_password = new_password
                    user.save()
                    messages.info(request, '修改成功！')
                else:
                    messages.info(request, '两次输入密码不一致！')
            else:
                messages.info(request, '旧密码输入错误！')

        return redirect('perioInfo', user_name=user_name, book_id=book_id)


def borrowBook(request, user_name, book_id):
    # 借书操作
    periodical = Periodical.objects.get(id=book_id)
    username = User.objects.get(user_name=user_name)

    Borrow.objects.create(user_name=username, book_id=periodical)

    periodical.residue -= 1
    periodical.save()
    messages.info(request, '借书成功！')

    return redirect('userPage', user_name=user_name)


def borrowShow(request, user_name):
    # 已借阅图书展示
    if request.method == 'GET':
        change_form = ChangeForm()
        borrowList = Borrow.objects.filter(user_name=user_name)
        periodical = Periodical.objects.all()
        periodicalIndex = PeriodicalIndex.objects.all()
        return render(request, 'login/hasborrow.html', {'borrowList': borrowList,
                                                        'perioindexList': periodicalIndex,
                                                        'perioList': periodical,
                                                        'username': user_name,
                                                        'ChangeForm': change_form})
    elif request.method == 'POST':
        change_form = ChangeForm(request.POST)
        if change_form.is_valid():
            old_password = change_form.cleaned_data['old_password']
            new_password = change_form.cleaned_data['new_password']
            confirm_password = change_form.cleaned_data['confirm_password']

            user = User.objects.get(user_name=user_name)
            if old_password == user.user_password:
                if new_password == confirm_password:
                    user.user_password = new_password
                    user.save()
                    messages.info(request, '修改成功！')
                else:
                    messages.info(request, '两次输入密码不一致！')
            else:
                messages.info(request, '旧密码输入错误！')

        return redirect('borrowShow', user_name=user_name)

def backBook(request, user_name, borrow_id):
    # 归还图书
    borrow = Borrow.objects.get(id=borrow_id)
    periodical = borrow.book_id

    borrow.back_date = datetime.datetime.now()
    borrow.save()

    periodical.residue += 1
    periodical.save()
    messages.info(request, '归还成功！')
    return redirect('borrowShow', user_name=user_name)

def adminPage(request, user_name):
    # 管理员界面
    if request.method == 'GET':
        change_form = ChangeForm()
        searchword = request.GET.get('search')
        if searchword:
            searchflag = request.GET.get('optionsRadios')
            if searchflag == "option1":
                # 书名查询
                periodical = Periodical.objects.all()
                periodicalIndex = PeriodicalIndex.objects.filter(name=searchword)
            elif searchflag == "option2":
                # 书籍编号查询
                periodical = Periodical.objects.filter(id=searchword)
                periodicalIndex = PeriodicalIndex.objects.all()
            elif searchflag == "option3":
                # 文章关键字查询
                article = PeriodicalInfo.objects.filter(Q(first_author=searchword) |
                                                        Q(second_author=searchword) |
                                                        Q(third_author=searchword) |
                                                        Q(forth_author=searchword) |
                                                        Q(first_keyword=searchword) |
                                                        Q(second_keyword=searchword) |
                                                        Q(third_keyword=searchword) |
                                                        Q(forth_keyword=searchword) |
                                                        Q(fifth_keyword=searchword) |
                                                        Q(paper_name=searchword))
                periodical = article.book_id
                periodicalIndex = PeriodicalIndex.objects.all()
        else:
            periodical = Periodical.objects.all()
            periodicalIndex = PeriodicalIndex.objects.all()

        return render(request, 'login/admin_main.html', {'perioindexList': periodicalIndex,
                                                         'perioList': periodical,
                                                         'username': user_name,
                                                         'ChangeForm': change_form})
    elif request.method == 'POST':
        change_form = ChangeForm(request.POST)
        if change_form.is_valid():
            old_password = change_form.cleaned_data['old_password']
            new_password = change_form.cleaned_data['new_password']
            confirm_password = change_form.cleaned_data['confirm_password']

            user = User.objects.get(user_name=user_name)
            if old_password == user.user_password:
                if new_password == confirm_password:
                    user.user_password = new_password
                    user.save()
                    messages.info(request, '修改成功！')
                else:
                    messages.info(request, '两次输入密码不一致！')
            else:
                messages.info(request, '旧密码输入错误！')

        return redirect('adminPage', user_name=user_name)


def adminPurchase(request, user_name):
    if request.method == 'GET':
        change_form = ChangeForm()
        purchaseList = Purchase.objects.all()
        return render(request, 'login/purchase.html', {'purchaseList':purchaseList,
                                                       'username':user_name,
                                                       'ChangeForm':change_form})

    elif request.method == 'POST':
        change_form = ChangeForm(request.POST)
        if change_form.is_valid():
            old_password = change_form.cleaned_data['old_password']
            new_password = change_form.cleaned_data['new_password']
            confirm_password = change_form.cleaned_data['confirm_password']

            user = User.objects.get(user_name=user_name)
            if old_password == user.user_password:
                if new_password == confirm_password:
                    user.user_password = new_password
                    user.save()
                    messages.info(request, '修改成功！')
                else:
                    messages.info(request, '两次输入密码不一致！')
            else:
                messages.info(request, '旧密码输入错误！')

        return redirect('adminPurchase', user_name=user_name)