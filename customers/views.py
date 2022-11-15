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
        context = {
            'id': customer.id,
            'form': form,
        }
        return render(request, 'customers/editCustomer.html', context)


def get_all_customers():
    
    # categories = get_object_or_404(Category,slug = category_slug)

    return Customer.objects.filter(is_active=True)

