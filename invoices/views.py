# from asyncio.windows_events import NULL
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from management.models import MngValues, MngStatus
from accounts.models import Account
from .forms import InvoiceForm
# from products.forms import InvoiceProdForm
from django.contrib import messages
from customers.models import Customer
from invoices.models import InvoiceDetail
from invoices.models import Invoice
from django.http import JsonResponse
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
from management.models import MngProductCategory
from .firmado import firmar_xml
from .xades import Xades
from zeep import Client
from .xmlBuildFactElect import XmlBuildFactElect
import requests

link_validacion_off = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl"
link_autorizacion_off = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl"

# link_validacion_online = "https://celcer.sri.gob.ec/comprobantes-electronicosws/RecepcionComprobantes?wsdl"
# link_autorizacion_online = "https://celcer.sri.gob.ec/comprobantes-electronicosws/AutorizacionComprobantes?wsdl"

cl_val_off = Client(link_validacion_off)
cl_aut_off = Client(link_autorizacion_off)

# cl_val_on = Client(link_validacion_online)
# cl_aut_on = Client(link_autorizacion_online)


@login_required(login_url='login')
def newInvoice(request):
    if request.method == 'POST':
        mng_status = MngStatus.objects.get(description='En Progreso')
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

            invoice_number = str(post.Invoice_no).zfill(9)

            post.Invoice_no_final = invoice_number
            post.mngStatus_id = mng_status

            post.save()
            # messages.success(request, 'Factura Creada....')
            return redirect('newInvoiceDetail', invoice_id=post.id)
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


@login_required(login_url='login')
def newInvoiceDetail(request, invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        invoice = None

    Invdetail = getAllActualInvoiceDetails(invoice)

    if request.method == 'POST':
        if request.POST.get("post_btn") == 'btn1':
            form = request.POST

            try:
                prod = Product.objects.get(product_code=form['product_code'])
            except Product.DoesNotExist:
                messages.error(request, 'Producto No Existe')
                return redirect('newInvoiceDetail', invoice_id=invoice_id)

            if prod.stock > 0:
                discountVal = 0
                quantityVal = int(form['quantity'])
                resultTotal = 0
                resultStock = 0
                flagProdInDetail = False

                if len(Invdetail) > 0:
                    prodQuantitySum = 0
                    for Inv in Invdetail:
                        if Inv.product_id == prod:
                            flagProdInDetail = True
                            prodQuantitySum = Inv.quantity + quantityVal
                            resultStock = prod.stock - prodQuantitySum

                            if resultStock > 0:
                                if Inv.product_id.is_discount:
                                    discountVal = calculateDiscount(Inv.product_id.price,
                                                                    Inv.product_id.discountPorcentage)
                                    discountVal = discountVal * prodQuantitySum
                                    resultTotal = Inv.product_id.price * prodQuantitySum - discountVal
                                else:
                                    discountVal = 0
                                    resultTotal = Inv.product_id.price * prodQuantitySum

                                Inv.quantity = prodQuantitySum
                                Inv.discount = discountVal
                                Inv.total_price = resultTotal
                                Inv.save()
                            else:
                                messages.error(request, 'Producto en actual factura tiene ' + str(
                                    Inv.quantity) + ' se quiere agregar ' + str(
                                    quantityVal) + ' el total en stock es ' + str(prod.stock))
                                return redirect('newInvoiceDetail', invoice_id=invoice_id)

                if flagProdInDetail:  # If product is already in the invoice detail attach a new one
                    InvdetailAct = getAllActualInvoiceDetails(invoice)
                    if len(InvdetailAct) > 0:
                        subtotal_12 = 0
                        subtotal_0 = 0
                        subtotalDisc = 0
                        taxsubtotal = 0
                        mng_tax = MngValues.objects.get(description='iva')
                        for invM in InvdetailAct:
                            if invM.product_id.is_0_tax:
                                subtotal_0 += invM.total_price
                            else:
                                subtotal_12 += invM.total_price
                            subtotalDisc += invM.discount
                        taxsubtotal = subtotal_12 * mng_tax.value / 100
                        # Alter Invoice Values
                        invoice.subtotal_0 = subtotal_0
                        invoice.subtotal_tax = subtotal_12
                        invoice.subtotal_no_taxes = subtotal_0 + subtotal_12
                        invoice.subtotal_discount = subtotalDisc
                        invoice.subtotal_tax_percentage = taxsubtotal
                        invoice.subtotal_gran_total = subtotal_0 + subtotal_12 + taxsubtotal - subtotalDisc
                        invoice.save()
                        return redirect('newInvoiceDetail', invoice_id=invoice_id)
                else:  # If product is not in the actual detail invoice
                    resultStock = prod.stock - quantityVal
                    if resultStock > 0:
                        if prod.is_discount:
                            discountVal = calculateDiscount(prod.price, prod.discountPorcentage)
                            discountVal = discountVal * quantityVal
                            resultTotal = prod.price * quantityVal - discountVal
                        else:
                            discountVal = 0
                            resultTotal = prod.price * quantityVal
                        inv_detail = InvoiceDetail.objects.create(
                            invoice_id=invoice,
                            product_id=prod,
                            quantity=quantityVal,
                            unit_price=prod.price,
                            discount=discountVal,
                            total_price=resultTotal,
                        )
                        inv_detail.save()
                        InvdetailAct = getAllActualInvoiceDetails(invoice)
                        if len(InvdetailAct) > 0:
                            subtotal_12 = 0
                            subtotal_0 = 0
                            subtotalDisc = 0
                            taxsubtotal = 0
                            mng_tax = MngValues.objects.get(description='iva')
                            for inv in InvdetailAct:
                                if inv.product_id.is_0_tax:
                                    subtotal_0 += inv.total_price
                                else:
                                    subtotal_12 += inv.total_price
                                subtotalDisc += inv.discount
                            taxsubtotal = subtotal_12 * mng_tax.value / 100
                            # Alter Invoice Values
                            invoice.subtotal_0 = subtotal_0
                            invoice.subtotal_tax = subtotal_12
                            invoice.subtotal_no_taxes = subtotal_0 + subtotal_12
                            invoice.subtotal_discount = subtotalDisc
                            invoice.subtotal_tax_percentage = taxsubtotal
                            invoice.subtotal_gran_total = subtotal_0 + subtotal_12 + taxsubtotal - subtotalDisc
                            invoice.save()
                            return redirect('newInvoiceDetail', invoice_id=invoice_id)
                    else:
                        messages.error(request, 'Producto tiene ' + str(prod.stock) + ' en Stock')
                        return redirect('newInvoiceDetail', invoice_id=invoice_id)
                # else:
            else:
                messages.error(request, 'Producto No en Stock')
                return redirect('newInvoiceDetail', invoice_id=invoice_id)

        else:
            id_prod = request.POST.get("code_prod", None)
            prod_quantity = int(request.POST.get("quantity", None))
            discountVal = 0
            resultTotal = 0
            stockTotal = 0

            if Invoice.objects.filter(id=invoice_id).exists():
                invoice_data_prod = Product.objects.get(product_code=id_prod)

                if InvoiceDetail.objects.filter(invoice_id=invoice, product_id=invoice_data_prod):
                    invoice_det_data = InvoiceDetail.objects.get(invoice_id=invoice, product_id=invoice_data_prod)
                    stockTotal = invoice_data_prod.stock - prod_quantity

                    if stockTotal > 0:
                        invoice_det_data.quantity = prod_quantity

                        if invoice_data_prod.is_discount:
                            discountVal = calculateDiscount(invoice_data_prod.price,
                                                            invoice_data_prod.discountPorcentage)
                            discountVal = discountVal * prod_quantity
                            resultTotal = invoice_data_prod.price * prod_quantity - discountVal
                        else:
                            discountVal = 0
                            resultTotal = invoice_data_prod.price * prod_quantity

                        invoice_det_data.discount = discountVal
                        invoice_det_data.total_price = resultTotal
                        invoice_det_data.save()

                        invDetailAct = getAllActualInvoiceDetails(invoice)
                        if len(invDetailAct) > 0:
                            subtotal_12 = 0
                            subtotal_0 = 0
                            subtotalDisc = 0
                            taxsubtotal = 0
                            mng_tax = MngValues.objects.get(description='iva')

                            for inv in invDetailAct:
                                if inv.product_id.is_0_tax:
                                    subtotal_0 += inv.total_price
                                else:
                                    subtotal_12 += inv.total_price

                                subtotalDisc += inv.discount

                            taxsubtotal = subtotal_12 * mng_tax.value / 100

                            # Alter Invoice Values
                            invoice.subtotal_0 = subtotal_0
                            invoice.subtotal_tax = subtotal_12
                            invoice.subtotal_no_taxes = subtotal_0 + subtotal_12
                            invoice.subtotal_discount = subtotalDisc
                            invoice.subtotal_tax_percentage = taxsubtotal
                            invoice.subtotal_gran_total = subtotal_0 + subtotal_12 + taxsubtotal - subtotalDisc
                            invoice.save()

                        return redirect('newInvoiceDetail', invoice_id=invoice_id)
                    else:
                        messages.error(request, 'Producto tiene ' + str(invoice_data_prod.stock) + ' en Stock')
                        return redirect('newInvoiceDetail', invoice_id=invoice_id)
                else:
                    messages.error(request, 'Detalle del Producto No Existe')
                    return redirect('newInvoiceDetail', invoice_id=invoice_id)
            else:
                messages.error(request, 'Error Invoice')
                return redirect('newInvoiceDetail', invoice_id=invoice_id)
    else:

        context = {
            'invoice': invoice,
            'invdetail': Invdetail,
        }
        return render(request, 'invoices/newInvoiceDetail.html', context)


def checkCustomerData(request):
    if request.method == "GET":
        id_cust = request.GET.get("id_customer", None)
        if Customer.objects.filter(id=id_cust).exists():
            customer_data = Customer.objects.get(pk=id_cust)
            return JsonResponse({"customer_full_name": customer_data.first_name + ' ' + customer_data.last_name,
                                 "customer_doc_num": customer_data.document_number,
                                 "customer_email": customer_data.email,
                                 "customer_phone1": customer_data.phone_1,
                                 "customer_address": customer_data.address,
                                 "customer_city": customer_data.mngCity_id.description}, status=200)
        else:
            return JsonResponse({}, status=400)


def calculateDiscount(amount, discount):
    if (amount > 0):
        valPorc = amount * discount
        valTot = valPorc / 100

        return valTot


@csrf_exempt
def deleteInvoiceDetail(request, invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        invoice = None

    if request.method == "GET":
        id_invoice = request.GET.get("id_invoice", None)
        id_prod = request.GET.get("id_prod", None)

        try:
            prod = Product.objects.get(product_code=id_prod)
        except Product.DoesNotExist:
            prod = None

        if InvoiceDetail.objects.filter(invoice_id=invoice, product_id=prod):
            invoice_det_data = InvoiceDetail.objects.get(invoice_id=invoice, product_id=prod)
            invoice_det_data.delete()

            Invdetail = getAllActualInvoiceDetails(invoice)

            if len(Invdetail) > 0:
                subtotal_12 = 0
                subtotal_0 = 0
                subtotalDisc = 0
                taxsubtotal = 0
                mng_tax = MngValues.objects.get(description='iva')
                for inv in Invdetail:
                    if inv.product_id.is_0_tax:
                        subtotal_0 += inv.total_price
                    else:
                        subtotal_12 += inv.total_price
                    subtotalDisc += inv.discount
                taxsubtotal = subtotal_12 * mng_tax.value / 100
                # Alter Invoice Values
                invoice.subtotal_0 = subtotal_0
                invoice.subtotal_tax = subtotal_12
                invoice.subtotal_no_taxes = subtotal_0 + subtotal_12
                invoice.subtotal_discount = subtotalDisc
                invoice.subtotal_tax_percentage = taxsubtotal
                invoice.subtotal_gran_total = subtotal_0 + subtotal_12 + taxsubtotal - subtotalDisc
                invoice.save()

            return JsonResponse({"message": "success"}, status=200)
            # return redirect('newInvoiceDetail',  invoice_id=invoice_id)
        else:
            messages.error(request, 'Error No se encuentra detalle factura')
            return redirect('newInvoiceDetail', invoice_id=invoice_id)


def getAllActualInvoiceDetails(invoice):
    return invoice.invoicedetail_set.all()


def generateInvoice(invoice_id):
    print(invoice_id)
    return redirect('newInvoiceDetail', invoice_id=invoice_id)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Opens up page as PDF Oder Page
class ViewPDF(View):

    def get(self, request, invoice_id, *args, **kwargs):

        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            invoice = None

        prodListidsCat = []

        InvdetailAct = InvoiceDetail.objects.filter(invoice_id=invoice_id)

        for invda in InvdetailAct:
            prodListidsCat.append(invda.product_id.mngProductCategory_id.id)

        # categories = MngProductCategory.objects.all()
        categories = MngProductCategory.objects.filter(id__in=prodListidsCat)

        context = {
            'invoice': invoice,
            'invdetail': InvdetailAct,
            'categories': categories,
        }

        pdf = render_to_pdf('invoices/pdf/invoiceOrder.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


# Fact Elect por probar
class DownloadXML(View):
    def get(self, request, invoice_id, *args, **kwargs):
        xmlInit = XmlBuildFactElect()
        xmlDoc = xmlInit.create(invoice_id)
        #firm = firmar_xml(xmlDoc[0]).encode()
        file_pk12 = "invoices/firma/5760703_identity.p12"
        password = "owq9128"
        xades = Xades()
        firm = xades.apply_digital_signature(xmlDoc[0],file_pk12,password)
        print(firm)
        #r = cl_val_off.service.validarComprobante(firm)
        #print(r)
        #auth = cl_aut_off.service.autorizacionComprobante(xmlDoc[1])
        #print(auth)
        # print(auth)
        # response = HttpResponse(xml, content_type='application/xml')
        # #filename = "Invoice_%s.xml" %("12341231")
        # content = "attachment; filename='%s'" %(xml)
        # response['Content-Disposition'] = content
        # return response
        return redirect('newInvoiceDetail', invoice_id=invoice_id)
