from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from .models import Customer


@login_required(login_url = 'login')
def newCustomer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # phone_1 = form.cleaned_data['phone_1']
            # phone_2 = form.cleaned_data['phone_2']
            # email = form.cleaned_data['email']
            # address = form.cleaned_data['address']
            # mngCity_id = form.cleaned_data['mngCity_id']
            # mngDocumentType_id = form.cleaned_data['mngDocumentType_id']
            # mngPersonType_id = form.cleaned_data['mngPersonType_id']
            # document_number = form.cleaned_data['document_number']
            # note = form.cleaned_data['note']

            form.save()

            messages.success(request, 'Cliente Creado....')
            return redirect('dashboard')

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
            messages.success(request, 'Cliente No ha sido Editado....')
            return redirect('viewCustomer')  
    else:
        form = CustomerForm(instance=customer)
        context = {
            'id': customer.id,
            'form': form,
        }
        return render(request, 'customers/editCustomer.html', context)


def get_all_customers():
    
    # categories = get_object_or_404(Category,slug = category_slug)

    return Customer.objects.filter(is_active=True)

