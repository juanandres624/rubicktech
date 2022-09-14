from django.urls import path
from . import views

urlpatterns = [
    path('newProvider', views.newProvider, name='newProvider'),
    path('viewProviders', views.viewProviders, name='viewProviders'),
    path('editProvider/<int:provider_id>/',views.editProvider,name='editProvider'),


]