"""PeriodicalManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from managesystem import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('login/user_main.html', views.userPage, name='userPage'),
    path(r'login/user_main/(?<user_name>)', views.userPage, name='userPage'),
    path(r'login/user_main/perioinfo/(?<user_name>)/(?<book_id>)', views.perioInfo, name='perioInfo'),
    path(r'login/user_main/borrow/(?<user_name>)/(?<book_id>)', views.borrowBook, name='borrowBook'),
    path(r'login/user_main/hasborrow/(?<user_name>)', views.borrowShow, name='borrowShow'),
    path(r'login/user_main/backBook/(?<user_name>)/(?<borrow_id>)', views.backBook, name='backBook'),
    path(r'login/user_main/changePass/(?<user_name>)', views.changePass, name='changePass'),
    path('admin/', admin.site.urls),
]
