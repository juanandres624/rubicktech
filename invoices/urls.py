from django.urls import path
from . import views
# from django.conf.urls.static import static
# from django.conf import settings
from invoices.views import (
    checkCustomerData,deleteInvoiceDetail
)

urlpatterns = [
    path('newInvoice', views.newInvoice, name='newInvoice'),
    path('get/ajax/validate/customer/', checkCustomerData, name = "ajax_customer_data"),
    path('newInvoice/<int:invoice_id>/',views.newInvoiceDetail, name='newInvoiceDetail'),
    path('newInvoice/<int:invoice_id>/delete/ajax/invoice/details/', deleteInvoiceDetail, name = "deleteInvoiceDetail"),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    #path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]