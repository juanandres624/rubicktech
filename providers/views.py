from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from providers.models import Provider
from .forms import ProviderForm
from products.models import Product
from accounts.models import Account
import sweetify

@login_required(login_url = 'login')
def newProvider(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.user = request.user.admin_id
            post.save()
            # messages.success(request, 'Proveedor Creado....')
            sweetify.success(request, 'Proveedor ha sido Creado')
            return redirect('editProvider', provider_id = post.id)
        else:
            # messages.error(request, form.errors)
            sweetify.error(request, form.errors)
            return redirect('newProvider')

    else:
        form = ProviderForm(request.POST or None, request.FILES or None)
        context = {
            'form': form,
        }

    return render(request, 'providers/newProvider.html', context)


@login_required(login_url = 'login')
def viewProviders(request):

    all_providers = get_all_providers(request.user.id)

    context = {
        'providers' : all_providers
    }

    return render(request, 'providers/viewProvider.html', context)

@login_required(login_url = 'login')
def editProvider(request,provider_id):

    try:
        userAdmin = Account.objects.get(pk=request.user.admin_id.id)
    except Exception as e:
        raise e

    try:
        provider = Provider.objects.get(pk=provider_id)
    except Exception as e:
        raise e

    if request.method == 'POST':
        form = ProviderForm(request.POST,instance= provider)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Proveedor Editado....')
            sweetify.success(request, 'Proveedor ha sido Editado')
            return redirect('editProvider', provider.id)
        else:
            # messages.success(request, 'Proveedor No ha sido Editado....')
            sweetify.error(request, 'Proveedor no ha sido Editado')
            return redirect('viewProvider')  
    else:
        if userAdmin == provider.user:
            form = ProviderForm(instance=provider)
            products = Product.objects.filter(provider_id=provider)

            context = {
                'id': provider.id,
                'form': form,
                'provider':provider,
                'prodProv':products,
            }
            return render(request, 'providers/editProvider.html', context)
        else:
            # messages.error(request, 'No hay Registros del Proveedor')
            sweetify.error(request, 'No hay Registros del Proveedor')
            return redirect('viewProviders')


def get_all_providers(user_id):

    try:
        UserAdmin = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        UserAdmin = None
    
    return Provider.objects.filter(user=UserAdmin.admin_id,is_active=True)
