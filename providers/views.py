from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from providers.models import Provider
from .forms import ProviderForm
from products.models import Product


@login_required(login_url = 'login')
def newProvider(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor Creado....')
            return redirect('dashboard')

    else:
        form = ProviderForm(request.POST or None, request.FILES or None)
        context = {
            'form': form,
        }

    return render(request, 'providers/newProvider.html', context)


@login_required(login_url = 'login')
def viewProviders(request):

    all_providers = get_all_providers()

    context = {
        'providers' : all_providers
    }

    return render(request, 'providers/viewProvider.html', context)

@login_required(login_url = 'login')
def editProvider(request,provider_id):

    try:
        provider = Provider.objects.get(pk=provider_id)
    except Exception as e:
        raise e

    if request.method == 'POST':
        form = ProviderForm(request.POST,instance= provider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor Editado....')
            return redirect('editProvider', provider.id)
        else:
            messages.success(request, 'Proveedor No ha sido Editado....')
            return redirect('viewProvider')  
    else:
        form = ProviderForm(instance=provider)
        products = Product.objects.filter(provider_id=provider)

        context = {
            'id': provider.id,
            'form': form,
            'provider':provider,
            'prodProv':products,
        }
        return render(request, 'providers/editProvider.html', context)


def get_all_providers():
    
    return Provider.objects.filter(is_active=True)
