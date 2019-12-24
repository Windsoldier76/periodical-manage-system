from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/user_main.html', views.userPage, name='userPage')
]