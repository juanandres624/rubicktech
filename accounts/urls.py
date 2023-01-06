from django.urls import path, include
from . import views
from accounts.views import (
    deleteUser
)

urlpatterns = [
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('newUser/', views.registerUser, name='newUser'),
    path('viewUsers/', views.viewUsers, name='viewUsers'),
    path('accounts/viewUsers/delete/ajax/account/users/', deleteUser, name = "deleteUser"),

]