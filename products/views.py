from ast import For
from dataclasses import field
from turtle import textinput
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductsForm,VariationForm,ImageForm,CatalogForm
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Product, Variation,Image

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

@login_required(login_url = 'login')
def editProduct(request,product_id):

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None
               
    variation = product.variation_set.all()
    image = product.image_set.all()

    if request.method == 'POST':
        form = ProductsForm(request.POST,instance= product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto Editado....')
            return redirect('editProduct', product.id)
        else:
            messages.success(request, 'Producto No ha sido Editado....')
            return redirect('editProduct', product.id)  
    else:
        form = ProductsForm(instance=product)
        context = {
            'id': product.id,
            'form': form,
            'variations':variation,
            'images':image,
        }
        return render(request, 'products/editProduct.html', context)


@login_required(login_url = 'login')
def createVariation(request,product_id):

    VariationFormSet = inlineformset_factory(Product,Variation,
    form=VariationForm, extra=8)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None

    formset = VariationFormSet(instance=product)

    if request.method == 'POST':
        formset = VariationFormSet(request.POST,instance=product)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Producto Editado....')
            return redirect('editProduct', product.id)
        else:
            messages.success(request, 'Producto No ha sido Editado....')
            return redirect('editProduct', product.id)  
    else:
        #form = VariationForm(instance=product)
        context = {
            'id': product.id,
            'formset': formset,
        }
        return render(request, 'products/productVariation.html', context)


@login_required(login_url = 'login')
def createImage(request,product_id):

    ImageFormSet = inlineformset_factory(Product,Image,
    form=ImageForm, extra=8)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None

    formset = ImageFormSet(instance=product)

    if request.method == 'POST':
        formset = ImageFormSet(request.POST,request.FILES,instance=product)
        if formset.is_valid():

            product.has_image = True
            product.save()
                
            formset.save()
            messages.success(request, 'Producto Editado....')
            return redirect('editProduct', product.id)
        else:
            messages.success(request, 'Producto No ha sido Editado....')
            return redirect('editProduct', product.id)  
    else:
        #form = VariationForm(instance=product)
        context = {
            'id': product.id,
            'formset': formset,
        }
        return render(request, 'products/productImages.html', context)

@login_required(login_url = 'login')
def viewProducts(request):

    all_products = get_all_products()
    img = []

    for products in all_products:

        try:
            product_img = Image.objects.get(product_id=products.id,default=True)
            img.append(product_img)

        except Image.DoesNotExist:
            product_img = None

    context = {
        'products' : all_products,
        'prod_img' : img
    }

    return render(request, 'products/viewProduct.html', context)


@login_required(login_url = 'login')
def viewCatalogs(request):

    if request.method == 'POST':
        form = CatalogForm(request.POST)
        if form.is_valid():


            # messages.success(request, 'Producto Creado....')
            return redirect('dashboard')

    else:
        form = CatalogForm(request.POST or None, request.FILES or None)
        context = {
            'form': form,
        }
    
    return render(request, 'products/viewCatalogs.html',context)


def get_all_products():
    
    return Product.objects.filter()
