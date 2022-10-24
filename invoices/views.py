from asyncio.windows_events import NULL
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InvoiceForm
from django.contrib import messages
from customers.models import Customer
from invoices.models import Invoice
from django.http import JsonResponse
from datetime import date


@login_required(login_url = 'login')
def newInvoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if post.is_paid:
                post.paid_date = str(date.today())
            else:
                post.paid_date = None

            if post.is_final_customer:
                final_cust = Customer.objects.get(document_number=0)
                post.billing_customer_id = final_cust

            year = post.created_date.strftime("%Y")
            month = post.created_date.strftime("%m")

            invoice_number = str(year) + str(month) + str(post.Invoice_no).zfill(6)

            post.Invoice_no_final = invoice_number

            post.save()
            #messages.success(request, 'Factura Creada....')
            return redirect('newInvoiceDetail',  invoice_id=post.id)
        else:
            messages.error(request, 'Error:' + form.errors)
            return redirect('dashboard')

    else:
        form = InvoiceForm(request.POST or None)
        context = {
            'form': form,
            'user': request.user,
        }

        return render(request, 'invoices/newInvoice.html', context)


@login_required(login_url = 'login')
def newInvoiceDetail(request,invoice_id):

    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        invoice = None
               
    if request.method == 'POST':

        pass 
    else:

        context = {
            'invoice': invoice,
        }
        return render(request, 'invoices/newInvoiceDetail.html', context)


def checkCustomerData(request):
    if request.method == "GET":
        id_cust = request.GET.get("id_customer", None)
        if Customer.objects.filter(id = id_cust).exists():
            customer_data = Customer.objects.get(pk = id_cust)
            return JsonResponse({"customer_full_name":customer_data.first_name + ' ' + customer_data.last_name,
                "customer_doc_num":customer_data.document_number,
                "customer_email":customer_data.email,
                "customer_phone1":customer_data.phone_1,
                "customer_address":customer_data.address,
                "customer_city":customer_data.mngCity_id.description}, status = 200)
        else:
            return JsonResponse({}, status = 400)

