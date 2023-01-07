from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductsForm,VariationForm,ImageForm,CatalogForm
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Product, Variation,Image
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from management.models import MngProductCategory,MngProductBrand
from django.http import JsonResponse
from accounts.models import Account

@login_required(login_url = 'login')
def newProduct(request):
    if request.method == 'POST':
        form = ProductsForm(request.user,request.POST, request.FILES or None)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.user = request.user.admin_id
            post.save()
            messages.success(request, 'Producto Creado....')
            return redirect('editProduct',  product_id=post.id)
    else:
        form = ProductsForm(request.user,request.POST or None, request.FILES or None)
        context = {
            'form': form,
        }

        return render(request, 'products/newProduct.html', context)

@login_required(login_url = 'login')
def editProduct(request,product_id):

    try:
        userAdmin = Account.objects.get(pk=request.user.admin_id.id)
    except Exception as e:
        raise e

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None
               
    # variation = product.variation_set.all()
    image = product.image_set.all()

    if request.method == 'POST':
        form = ProductsForm(request.user,request.POST,instance= product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto Editado....')
            return redirect('editProduct', product.id)
        else:
            messages.success(request, 'Producto No ha sido Editado....')
            return redirect('editProduct', product.id)  
    else:
        if userAdmin == product.user:
            form = ProductsForm(request.user,instance=product)
            context = {
                'id': product.id,
                'form': form,
                # 'variations':variation,
                'images':image,
            }
            return render(request, 'products/editProduct.html', context)
        else:
            messages.error(request, 'No hay Registros del Producto')
            return redirect('viewProducts')


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

    all_products = get_all_products(request.user.id)
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

    if request.GET:
        prod_name = request.GET['product_name']
        prod_price = request.GET['price']
        prod_categ = request.GET['mngProductCategory_id']
        prod_provider = request.GET['provider_id']
        prod_brand = request.GET['mngProductBrand_id']

        if prod_name :
            prod_name_condition = Q(product_name__icontains=prod_name)
        else:
            prod_name_condition = Q()

        if prod_price :
            prod_price_condition = Q(price__exact=prod_price)
        else:
            prod_price_condition = Q()

        if prod_categ :
            prod_categ_condition = Q(mngProductCategory_id__exact=prod_categ)
        else:
            prod_categ_condition = Q()        
            
        if prod_provider :
            prod_provider_condition = Q(prod_provider__exact=prod_provider)
        else:
            prod_provider_condition = Q()        
            
        if prod_brand :
            prod_brand_condition = Q(prod_brand__exact=prod_brand)
        else:
            prod_brand_condition = Q()

        products = Product.objects.order_by('-created_date').filter(
            prod_name_condition & prod_price_condition & prod_categ_condition & prod_provider_condition & 
            prod_brand_condition)


        form = CatalogForm(request.GET or None)
        context = {
            'form': form,
        }

    else:
        form = CatalogForm(request.GET or None)
        context = {
            'form': form,
        }
    
    return render(request, 'products/viewCatalogs.html',context)


def get_all_products(user_id):

    try:
        UserAdmin = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        UserAdmin = None
    
    return Product.objects.filter(user=UserAdmin.admin_id,is_active=True)

@csrf_exempt
def addCategory(request):
    if request.method == "POST":
        cat_desc = request.POST.get('cat_desc')
        cat_id = MngProductCategory.objects.create(description=cat_desc)
        cat_id.created_by = request.user
        cat_id.user = request.user.admin_id
        cat_id.save()
        return HttpResponse(cat_id.id)

def getCategoryById(request,id):
    if request.method == "GET":
        id_categ = MngProductCategory.objects.get(pk=id)
        if MngProductCategory.objects.filter(id=id).exists():
            return JsonResponse({"id": id_categ.id,
                                 "description": id_categ.description}, status=200)
        else:
            return JsonResponse({}, status=400)

    return HttpResponse(JsonResponse)

@csrf_exempt
def addBrand(request):
    if request.method == "POST":
        brand_desc = request.POST.get('brand_desc')
        brand_id = MngProductBrand.objects.create(description=brand_desc)
        brand_id.created_by = request.user
        brand_id.user = request.user.admin_id
        brand_id.save()
        return HttpResponse(brand_id.id)

def getBrandById(request,id):
    if request.method == "GET":
        id_brand = MngProductBrand.objects.get(pk=id)
        if MngProductBrand.objects.filter(id=id).exists():
            return JsonResponse({"id": id_brand.id,
                                 "description": id_brand.description}, status=200)
        else:
            return JsonResponse({}, status=400)

    return HttpResponse(JsonResponse)
