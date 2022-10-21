from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import InvoiceForm
from django.contrib import messages
from customers.models import Customer
from django.http import JsonResponse



@login_required(login_url = 'login')
def newInvoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():

            form.save()

            messages.success(request, 'Venta Creada....')
            return redirect('dashboard')

    else:
        form = InvoiceForm(request.POST or None, request.FILES or None, initial={'user': request.user})
        context = {
            'form': form,
        }

        return render(request, 'invoices/newInvoice.html', context)


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

