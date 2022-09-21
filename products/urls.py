from django.urls import path
from . import views

urlpatterns = [
    path('newProduct', views.newProduct, name='newProduct'),

]