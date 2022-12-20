from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from .models import Customer
from invoices.models import Invoice
from django.http import JsonResponse
import requests


@login_required(login_url = 'login')
def newCustomer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Cliente Creado....')
            return redirect('editCustomer', customer_id = post.id)
        else:
            messages.error(request, form.errors)
            return redirect('newCustomer')
    else:
        form = CustomerForm(request.POST or None, request.FILES or None)
        context = {
            'form': form,
        }

    return render(request, 'customers/newCustomer.html', context)


@login_required(login_url = 'login')
def viewCustomers(request):

    all_customers = get_all_customers()

    context = {
        'customers' : all_customers
    }

    return render(request, 'customers/viewCustomer.html', context)
    
    
@login_required(login_url = 'login')
def editCustomer(request,customer_id):

    try:
        customer = Customer.objects.get(pk=customer_id)
    except Exception as e:
        raise e

    if request.method == 'POST':
        form = CustomerForm(request.POST,instance= customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente Editado....')
            return redirect('editCustomer', customer.id)
        else:
            messages.error(request, form.errors)
            return redirect('editCustomer', customer.id)
    else:
        form = CustomerForm(instance=customer)
        invoices = Invoice.objects.filter(billing_customer_id=customer)
        #InvdetailAct = Invoice.objects.filter(invoice_id=invoice_id)
        context = {
            'id': customer.id,
            'form': form,
            'customer': customer,
            'invoices': invoices,
        }
        return render(request, 'customers/editCustomer.html', context)


def get_all_customers():
    
    # categories = get_object_or_404(Category,slug = category_slug)

    return Customer.objects.filter(is_active=True)


# def checkCustomerDataSri(request):
#     if request.method == "GET":
#         doc_numb = request.GET.get("num_doc", None)

#         reCaptcha_response = reCaptchaV3('https://www.google.com/recaptcha/api2/userverify?k=6Lc6rokUAAAAAJBG2M1ZM1LIgJ85DwbSNNjYoLDk')
#         print(reCaptcha_response)
#         url = 'https://www.google.com/recaptcha/api2/userverify?k=6Lc6rokUAAAAAJBG2M1ZM1LIgJ85DwbSNNjYoLDk'
#         FullUrlPath = '{}'.format(url)
#         #payload = {"numeroRuc": "{}".format(logModule),"message": "{}".format(logMessage)}
#         #headers = {'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJERUNMQVJBQ0lPTkVTIiwiaWF0IjoxNjcxMjE0OTk1LCJzdWIiOiJERUNMQVJBVE9SSUEgUFJFU0NSSVBDSU9OIEhFUkVOQ0lBIiwiZXhwIjoxNjcxMjE1NTk1fQ.ykPihI2lb-QWf9zdlZP6e8SArFhr7Kwpn7Dufm1mCnM'}
#         r = requests.post(FullUrlPath)
        # data = getRucDataSri(doc_numb)
        
        # print(r.text)
        # if Customer.objects.filter(id=id_cust).exists():
        #     customer_data = Customer.objects.get(pk=id_cust)
        #     return JsonResponse({"customer_full_name": customer_data.first_name + ' ' + customer_data.last_name,
        #                          "customer_doc_num": customer_data.document_number,
        #                          "customer_email": customer_data.email,
        #                          "customer_phone1": customer_data.phone_1,
        #                          "customer_address": customer_data.address,
        #                          "customer_city": customer_data.mngCity_id.description}, status=200)
        # else:
        #     return JsonResponse({}, status=400)

# def getRucDataSri(ruc):
#     url = 'https://srienlinea.sri.gob.ec/sri-catastro-sujeto-servicio-internet/rest/ConsolidadoContribuyente/obtenerPorNumerosRuc?&ruc='
#     FullUrlPath = '{}{}'.format(url,ruc)
#     #payload = {"numeroRuc": "{}".format(logModule),"message": "{}".format(logMessage)}
#     headers = {'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJERUNMQVJBQ0lPTkVTIiwiaWF0IjoxNjcxMjE0OTk1LCJzdWIiOiJERUNMQVJBVE9SSUEgUFJFU0NSSVBDSU9OIEhFUkVOQ0lBIiwiZXhwIjoxNjcxMjE1NTk1fQ.ykPihI2lb-QWf9zdlZP6e8SArFhr7Kwpn7Dufm1mCnM'}
#     r = requests.get(FullUrlPath, headers=headers)

#     #print(r)

#     return r.json()