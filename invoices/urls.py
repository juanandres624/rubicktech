from django.urls import path
from . import views
# from django.conf.urls.static import static
# from django.conf import settings
from invoices.views import (
    checkCustomerData
)

urlpatterns = [
    path('newInvoice', views.newInvoice, name='newInvoice'),
    path('get/ajax/validate/customer/', checkCustomerData, name = "ajax_customer_data"),
    path('newInvoice/<int:invoice_id>/',views.newInvoiceDetail, name='newInvoiceDetail'),

]