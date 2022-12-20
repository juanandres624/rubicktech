from django.urls import path
from . import views
# from customers.views import (
#     checkCustomerDataSri
# )

urlpatterns = [
    #path('', views.customers, name='customer'),
    path('newCustomer', views.newCustomer, name='newCustomer'),
    path('viewCustomers', views.viewCustomers, name='viewCustomers'),
    path('editCustomer/<int:customer_id>/',views.editCustomer,name='editCustomer'),
    # path('get/ajax/validate/customerSri/', checkCustomerDataSri, name = "ajax_customer_data_sri"),



]