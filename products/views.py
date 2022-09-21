from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductsForm
from django.contrib import messages

@login_required(login_url = 'login')
def newProduct(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST)
        if form.is_valid():

            form.save()

            messages.success(request, 'Producto Creado....')
            return redirect('dashboard')

    else:
        form = ProductsForm(request.POST or None, request.FILES or None)
        context = {
            'form': form,
        }

        return render(request, 'products/newProduct.html', context)
