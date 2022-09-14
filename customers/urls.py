from django.urls import path
from . import views

urlpatterns = [
    #path('', views.customers, name='customer'),
    path('newCustomer', views.newCustomer, name='newCustomer'),
    path('viewCustomers', views.viewCustomers, name='viewCustomers'),
    path('editCustomer/<int:customer_id>/',views.editCustomer,name='editCustomer'),


]