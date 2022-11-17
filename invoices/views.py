from asyncio.windows_events import NULL
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from management.models import MngValues,MngStatus,MngFactElect
from accounts.models import Account
from .forms import InvoiceForm
#from products.forms import InvoiceProdForm
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
from xml.dom import minidom
import os
import base64
import subprocess
import logging
from datetime import datetime
import itertools

@login_required(login_url = 'login')
def newInvoice(request):
    if request.method == 'POST':
        mng_status = MngStatus.objects.get(description ='En Progreso')
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
            #messages.success(request, 'Factura Creada....')
            return redirect('newInvoiceDetail',  invoice_id=post.id)
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


@login_required(login_url = 'login')
def newInvoiceDetail(request,invoice_id):
    
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
                return redirect('newInvoiceDetail',  invoice_id=invoice_id)

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
                                    discountVal = calculateDiscount(Inv.product_id.price,Inv.product_id.discountPorcentage)
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
                                messages.error(request, 'Producto en actual factura tiene ' + str(Inv.quantity) + ' se quiere agregar ' + str(quantityVal) + ' el total en stock es ' + str(prod.stock) )
                                return redirect('newInvoiceDetail',  invoice_id=invoice_id)

                if flagProdInDetail: #If product is already in the invoice detail attach a new one
                    InvdetailAct = getAllActualInvoiceDetails(invoice)
                    if len(InvdetailAct) > 0:
                        subtotal_12 = 0
                        subtotal_0 = 0
                        subtotalDisc = 0
                        taxsubtotal = 0
                        mng_tax = MngValues.objects.get(description ='iva')
                        for invM in InvdetailAct:
                            if invM.product_id.is_0_tax:
                                subtotal_0 += invM.total_price
                            else:
                                subtotal_12 += invM.total_price
                            subtotalDisc += invM.discount
                        taxsubtotal = subtotal_12 * mng_tax.value / 100
                        #Alter Invoice Values
                        invoice.subtotal_0 = subtotal_0
                        invoice.subtotal_tax = subtotal_12
                        invoice.subtotal_no_taxes = subtotal_0 + subtotal_12
                        invoice.subtotal_discount = subtotalDisc
                        invoice.subtotal_tax_percentage = taxsubtotal
                        invoice.subtotal_gran_total = subtotal_0 + subtotal_12 + taxsubtotal - subtotalDisc
                        invoice.save()                           
                        return redirect('newInvoiceDetail',  invoice_id=invoice_id)
                else: # If product is not in the actual detail invoice
                    resultStock = prod.stock - quantityVal
                    if resultStock > 0:
                        if prod.is_discount:
                            discountVal = calculateDiscount(prod.price,prod.discountPorcentage)
                            discountVal = discountVal * quantityVal
                            resultTotal = prod.price * quantityVal - discountVal
                        else:
                            discountVal = 0
                            resultTotal = prod.price * quantityVal             
                        inv_detail = InvoiceDetail.objects.create(
                            invoice_id=invoice,
                            product_id=prod,
                            quantity=quantityVal,
                            unit_price = prod.price,
                            discount = discountVal,
                            total_price = resultTotal,
                        )
                        inv_detail.save()
                        InvdetailAct = getAllActualInvoiceDetails(invoice)
                        if len(InvdetailAct) > 0:
                            subtotal_12 = 0
                            subtotal_0 = 0
                            subtotalDisc = 0
                            taxsubtotal = 0
                            mng_tax = MngValues.objects.get(description ='iva')
                            for inv in InvdetailAct:
                                if inv.product_id.is_0_tax:
                                    subtotal_0 += inv.total_price
                                else:
                                    subtotal_12 += inv.total_price
                                subtotalDisc += inv.discount
                            taxsubtotal = subtotal_12 * mng_tax.value / 100
                            #Alter Invoice Values
                            invoice.subtotal_0 = subtotal_0
                            invoice.subtotal_tax = subtotal_12
                            invoice.subtotal_no_taxes = subtotal_0 + subtotal_12
                            invoice.subtotal_discount = subtotalDisc
                            invoice.subtotal_tax_percentage = taxsubtotal
                            invoice.subtotal_gran_total = subtotal_0 + subtotal_12 + taxsubtotal - subtotalDisc
                            invoice.save()
                            return redirect('newInvoiceDetail',  invoice_id=invoice_id)
                    else:
                        messages.error(request, 'Producto tiene ' + str(prod.stock) + ' en Stock')
                        return redirect('newInvoiceDetail',  invoice_id=invoice_id)
                #else:
            else:
                messages.error(request, 'Producto No en Stock')
                return redirect('newInvoiceDetail',  invoice_id=invoice_id)

        else:
            id_prod = request.POST.get("code_prod", None)
            prod_quantity = int(request.POST.get("quantity", None))
            discountVal = 0
            resultTotal = 0
            stockTotal = 0

            if Invoice.objects.filter(id = invoice_id).exists():
                invoice_data_prod = Product.objects.get(product_code = id_prod)

                if InvoiceDetail.objects.filter(invoice_id = invoice, product_id = invoice_data_prod):
                    invoice_det_data = InvoiceDetail.objects.get(invoice_id = invoice, product_id = invoice_data_prod)
                    stockTotal = invoice_data_prod.stock - prod_quantity
                    
                    if stockTotal > 0:
                        invoice_det_data.quantity = prod_quantity

                        if invoice_data_prod.is_discount:
                            discountVal = calculateDiscount(invoice_data_prod.price,invoice_data_prod.discountPorcentage)
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
                            mng_tax = MngValues.objects.get(description ='iva')

                            for inv in invDetailAct:
                                if inv.product_id.is_0_tax:
                                    subtotal_0 += inv.total_price
                                else:
                                    subtotal_12 += inv.total_price

                                subtotalDisc += inv.discount

                            taxsubtotal = subtotal_12 * mng_tax.value / 100

                            #Alter Invoice Values
                            invoice.subtotal_0 = subtotal_0
                            invoice.subtotal_tax = subtotal_12
                            invoice.subtotal_no_taxes = subtotal_0 + subtotal_12
                            invoice.subtotal_discount = subtotalDisc
                            invoice.subtotal_tax_percentage = taxsubtotal
                            invoice.subtotal_gran_total = subtotal_0 + subtotal_12 + taxsubtotal - subtotalDisc
                            invoice.save()
                        
                        return redirect('newInvoiceDetail',  invoice_id=invoice_id)
                    else:
                        messages.error(request, 'Producto tiene ' + str(invoice_data_prod.stock) + ' en Stock')
                        return redirect('newInvoiceDetail',  invoice_id=invoice_id) 
                else:
                    messages.error(request, 'Detalle del Producto No Existe')
                    return redirect('newInvoiceDetail',  invoice_id=invoice_id)
            else:
                messages.error(request, 'Error Invoice')
                return redirect('newInvoiceDetail',  invoice_id=invoice_id)
    else:

        context = {
            'invoice': invoice,
            'invdetail': Invdetail,
        }
        return render(request, 'invoices/newInvoiceDetail.html',context)


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

def calculateDiscount(amount,discount):
    if(amount>0):
        valPorc = amount * discount
        valTot = valPorc / 100

        return valTot

@csrf_exempt
def deleteInvoiceDetail(request,invoice_id):

    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        invoice = None

    if request.method == "GET":
        id_invoice = request.GET.get("id_invoice", None)
        id_prod = request.GET.get("id_prod", None)

        try:
            prod = Product.objects.get(product_code = id_prod)
        except Product.DoesNotExist:
            prod = None

        if InvoiceDetail.objects.filter(invoice_id = invoice, product_id = prod):
            invoice_det_data = InvoiceDetail.objects.get(invoice_id = invoice, product_id = prod)
            invoice_det_data.delete()

            Invdetail = getAllActualInvoiceDetails(invoice)

            if len(Invdetail) > 0:
                subtotal_12 = 0
                subtotal_0 = 0
                subtotalDisc = 0
                taxsubtotal = 0
                mng_tax = MngValues.objects.get(description ='iva')
                for inv in Invdetail:
                    if inv.product_id.is_0_tax:
                        subtotal_0 += inv.total_price
                    else:
                        subtotal_12 += inv.total_price
                    subtotalDisc += inv.discount
                taxsubtotal = subtotal_12 * mng_tax.value / 100
                #Alter Invoice Values
                invoice.subtotal_0 = subtotal_0
                invoice.subtotal_tax = subtotal_12
                invoice.subtotal_no_taxes = subtotal_0 + subtotal_12
                invoice.subtotal_discount = subtotalDisc
                invoice.subtotal_tax_percentage = taxsubtotal
                invoice.subtotal_gran_total = subtotal_0 + subtotal_12 + taxsubtotal - subtotalDisc
                invoice.save()

            return JsonResponse({"message":"success"}, status = 200)
            #return redirect('newInvoiceDetail',  invoice_id=invoice_id)
        else:
            messages.error(request, 'Error No se encuentra detalle factura')
            return redirect('newInvoiceDetail',  invoice_id=invoice_id)


def getAllActualInvoiceDetails(invoice):
    return invoice.invoicedetail_set.all()

def generateInvoice(invoice_id):
    print(invoice_id)
    return redirect('newInvoiceDetail',  invoice_id=invoice_id)


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


def createFactElectXml(invoice_id):

    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        invoice = None

    Invdetail = getAllActualInvoiceDetails(invoice)

    mng_fact_properties = MngFactElect.objects.get(is_active = True)
    mainAccnt = Account.objects.get(is_superadmin = True)

    tipAmb = mng_fact_properties.tipoAmbiente

    # current dateTime
    now = datetime.now()
    tipComp = mng_fact_properties.tipoComprobante
    numRuc = str(mainAccnt.numRuc)
    razSoc = mainAccnt.razSocial
    nombCome = mainAccnt.nombCom
    dirMatr = mainAccnt.dirMatr
    dirEstab = mainAccnt.dirEstablec
    contribEspec = mainAccnt.contribEspec
    obligContab = ''
    if mainAccnt.obligContab:
        obligContab = 'SI'
    else:
       obligContab = 'NO' 
    serie = '001001'
    estab = '001' # Creo que establecimiento
    ptoEmi = '001' # Creo que punto de emision
    numSec = str(invoice.Invoice_no).zfill(9)
    codNum = numSec[1:]
    tipEmi = mng_fact_properties.tipoEmision
    tipIdentCompr = invoice.billing_customer_id.mngDocumentType_id.description
    flagGuiaRemis = False
    guiaRem = ''
    if flagGuiaRemis:
        guiaRem = '001-001-000000001' # Ejemplo de Guia de Remision
    razSocialComp = invoice.billing_customer_id.first_name + ' ' + invoice.billing_customer_id.last_name
    identifCompr = invoice.billing_customer_id.document_number
    direccCompr = invoice.billing_customer_id.address
    totalSinImp = invoice.subtotal_no_taxes
    totalDesc = invoice.subtotal_discount
    totalImpCod = mng_fact_properties.codImp
    totalImpTarifIva = mng_fact_properties.tarifIva
    totalImpBaseImp = totalSinImp - totalDesc
    totalImpValor = totalImpBaseImp * 12 / 100
    importeTotal = totalImpBaseImp + totalImpValor

    clavAcc = f'{now.strftime("%d%m%Y"):8.8}' + f'{tipComp:2.2}' + f'{numRuc:13.13}' + f'{tipAmb:1.1}' + f'{serie:6.6}' + f'{numSec:9.9}' + f'{codNum:8.8}' + f'{tipEmi:1.1}'
    digVerif = str(GenClavAccMod11(clavAcc))
    clavAccFinal = clavAcc + digVerif

    rootNode = minidom.Document()
    rootNode.toprettyxml(encoding="utf-8")
  
    factNode = rootNode.createElement('factura') 
    factNode.setAttribute('id', 'comprobante')
    factNode.setAttribute('version', '1.0.0')
    rootNode.appendChild(factNode)
    

    infoTribNode = rootNode.createElement('infoTributaria')
    factNode.appendChild(infoTribNode)

    ambienteNode = rootNode.createElement('ambiente')
    ambienteNodeTxt = rootNode.createTextNode(tipAmb)
    ambienteNode.appendChild(ambienteNodeTxt)
    infoTribNode.appendChild(ambienteNode)

    tipEmisNode = rootNode.createElement('tipoEmision')
    tipEmisNodeTxt = rootNode.createTextNode(tipEmi)
    tipEmisNode.appendChild(tipEmisNodeTxt)
    infoTribNode.appendChild(tipEmisNode)

    razSocNode = rootNode.createElement('razonSocial')
    razSocNodeTxt = rootNode.createTextNode(razSoc)
    razSocNode.appendChild(razSocNodeTxt)
    infoTribNode.appendChild(razSocNode)

    nomComNode = rootNode.createElement('nombreComercial')
    nomComNodeTxt = rootNode.createTextNode(nombCome)
    nomComNode.appendChild(nomComNodeTxt)
    infoTribNode.appendChild(nomComNode)    
    
    rucNode = rootNode.createElement('ruc')
    rucNodeTxt = rootNode.createTextNode(numRuc)
    rucNode.appendChild(rucNodeTxt)
    infoTribNode.appendChild(rucNode)    
    
    clavAccNode = rootNode.createElement('claveAcceso')
    clavAccNodeTxt = rootNode.createTextNode(clavAccFinal)
    clavAccNode.appendChild(clavAccNodeTxt)
    infoTribNode.appendChild(clavAccNode)

    codDocItNode = rootNode.createElement('codDoc')
    codDocItNodeTxt = rootNode.createTextNode(tipComp)
    codDocItNode.appendChild(codDocItNodeTxt)
    infoTribNode.appendChild(codDocItNode)   
    
    estabNode = rootNode.createElement('estab')
    estabNodeTxt = rootNode.createTextNode(estab)
    estabNode.appendChild(estabNodeTxt)
    infoTribNode.appendChild(estabNode)    
    
    ptoEmiNode = rootNode.createElement('ptoEmi')
    ptoEmiNodeTxt = rootNode.createTextNode(ptoEmi)
    ptoEmiNode.appendChild(ptoEmiNodeTxt)
    infoTribNode.appendChild(ptoEmiNode)    
    
    secuencialNode = rootNode.createElement('secuencial')
    secuencialNodeTxt = rootNode.createTextNode(numSec)
    secuencialNode.appendChild(secuencialNodeTxt)
    infoTribNode.appendChild(secuencialNode)    
    
    dirMatrizNode = rootNode.createElement('dirMatriz')
    dirMatrizNodeTxt = rootNode.createTextNode(dirMatr)
    dirMatrizNode.appendChild(dirMatrizNodeTxt)
    infoTribNode.appendChild(dirMatrizNode)    
    
    dirMatrizNode = rootNode.createElement('dirMatriz')
    dirMatrizNodeTxt = rootNode.createTextNode(dirMatr)
    dirMatrizNode.appendChild(dirMatrizNodeTxt)
    infoTribNode.appendChild(dirMatrizNode)

    infoFactNode = rootNode.createElement('infoFactura')
    factNode.appendChild(infoFactNode)

    fechaEmisionNode = rootNode.createElement('fechaEmision')
    fechaEmisionNodeTxt = rootNode.createTextNode(f'{now.strftime("%d/%m/%Y")}')
    fechaEmisionNode.appendChild(fechaEmisionNodeTxt)
    infoFactNode.appendChild(fechaEmisionNode)

    dirEstablecimientoNode = rootNode.createElement('dirEstablecimiento')
    dirEstablecimientoNodeTxt = rootNode.createTextNode(dirEstab)
    dirEstablecimientoNode.appendChild(dirEstablecimientoNodeTxt)
    infoFactNode.appendChild(dirEstablecimientoNode)

    if mainAccnt.obligContab:
        contribuyenteEspecialNode = rootNode.createElement('contribuyenteEspecial')
        contribuyenteEspecialNodeTxt = rootNode.createTextNode(contribEspec)
        contribuyenteEspecialNode.appendChild(contribuyenteEspecialNodeTxt)
        infoFactNode.appendChild(contribuyenteEspecialNode)

        obligadoContabilidadNode = rootNode.createElement('obligadoContabilidad')
        obligadoContabilidadNodeTxt = rootNode.createTextNode(obligContab)
        obligadoContabilidadNode.appendChild(obligadoContabilidadNodeTxt)
        infoFactNode.appendChild(obligadoContabilidadNode)
    else:
        obligadoContabilidadNode = rootNode.createElement('obligadoContabilidad')
        obligadoContabilidadNodeTxt = rootNode.createTextNode(obligContab)
        obligadoContabilidadNode.appendChild(obligadoContabilidadNodeTxt)
        infoFactNode.appendChild(obligadoContabilidadNode)

    tipIdentifComprNode = rootNode.createElement('tipoIdentificacionComprador')
    tipIdentifComprNodeTxt = rootNode.createTextNode(tipIdentCompr)
    tipIdentifComprNode.appendChild(tipIdentifComprNodeTxt)
    infoFactNode.appendChild(tipIdentifComprNode)

    if flagGuiaRemis:
        guiaRemisionNode = rootNode.createElement('guiaRemision')
        guiaRemisionNodeTxt = rootNode.createTextNode(guiaRem)
        guiaRemisionNode.appendChild(guiaRemisionNodeTxt)
        infoFactNode.appendChild(guiaRemisionNode)

    razSocialComprNode = rootNode.createElement('razonSocialComprador')
    razSocialComprNodeTxt = rootNode.createTextNode(razSocialComp)
    razSocialComprNode.appendChild(razSocialComprNodeTxt)
    infoFactNode.appendChild(razSocialComprNode)    
    
    identifComprNode = rootNode.createElement('identificacionComprador')
    identifComprNodeTxt = rootNode.createTextNode(identifCompr)
    identifComprNode.appendChild(identifComprNodeTxt)
    infoFactNode.appendChild(identifComprNode)    
    
    direccComprNode = rootNode.createElement('direccionComprador')
    direccComprNodeTxt = rootNode.createTextNode(direccCompr)
    direccComprNode.appendChild(direccComprNodeTxt)
    infoFactNode.appendChild(direccComprNode)
    
    totalSinImpNode = rootNode.createElement('totalSinImpuestos')
    totalSinImpNodeTxt = rootNode.createTextNode(str(totalSinImp))
    totalSinImpNode.appendChild(totalSinImpNodeTxt)
    infoFactNode.appendChild(totalSinImpNode)
    
    totalDescNode = rootNode.createElement('totalDescuento')
    totalDescNodeTxt = rootNode.createTextNode(str(totalDesc))
    totalDescNode.appendChild(totalDescNodeTxt)
    infoFactNode.appendChild(totalDescNode)

    #totalConImpuestos Node
    totalConImpNode = rootNode.createElement('totalConImpuestos')
    factNode.appendChild(totalConImpNode)

    #totalImpuesto Node
    totalImpNode = rootNode.createElement('totalImpuesto')
    totalConImpNode.appendChild(totalImpNode)

    totalImpCodNode = rootNode.createElement('codigo')
    totalImpCodNodeTxt = rootNode.createTextNode(totalImpCod)
    totalImpCodNode.appendChild(totalImpCodNodeTxt)
    totalImpNode.appendChild(totalImpCodNode)

    totalImpTarifIvaNode = rootNode.createElement('codigoPorcentaje')
    totalImpTarifIvaNodeTxt = rootNode.createTextNode(totalImpTarifIva)
    totalImpTarifIvaNode.appendChild(totalImpTarifIvaNodeTxt)
    totalImpNode.appendChild(totalImpTarifIvaNode)

    totalImpBaseImpoNode = rootNode.createElement('baseImponible')
    totalImpBaseImpoNodeTxt = rootNode.createTextNode(str(totalImpBaseImp))
    totalImpBaseImpoNode.appendChild(totalImpBaseImpoNodeTxt)
    totalImpNode.appendChild(totalImpBaseImpoNode)    
    
    totalImpValorNode = rootNode.createElement('valor')
    totalImpValorNodeTxt = rootNode.createTextNode(str(totalImpValor))
    totalImpValorNode.appendChild(totalImpValorNodeTxt)
    totalImpNode.appendChild(totalImpValorNode)

    propinaNode = rootNode.createElement('propina')
    propinaNodeTxt = rootNode.createTextNode('0.00')
    propinaNode.appendChild(propinaNodeTxt)
    infoFactNode.appendChild(propinaNode)

    importeTotalNode = rootNode.createElement('importeTotal')
    importeTotalNodeTxt = rootNode.createTextNode(str(importeTotal))
    importeTotalNode.appendChild(importeTotalNodeTxt)
    infoFactNode.appendChild(importeTotalNode)

    monedaNode = rootNode.createElement('moneda')
    monedaNodeTxt = rootNode.createTextNode('DÓLAR')
    monedaNode.appendChild(monedaNodeTxt)
    infoFactNode.appendChild(monedaNode)

    #detalles Node
    detallesNode = rootNode.createElement('detalles')
    factNode.appendChild(detallesNode)

    for deta in Invdetail:

        #detalle Node 
        detalleNode = rootNode.createElement('detalle')
        detallesNode.appendChild(detalleNode)

        codigoPrincipalNode = rootNode.createElement('codigoPrincipal')
        codigoPrincipalNodeTxt = rootNode.createTextNode(deta.product_id.product_code)
        codigoPrincipalNode.appendChild(codigoPrincipalNodeTxt)
        detalleNode.appendChild(codigoPrincipalNode)

        codigoSecNode = rootNode.createElement('codigoAuxiliar')
        codigoSecNodeTxt = rootNode.createTextNode(deta.product_id.code)
        codigoSecNode.appendChild(codigoSecNodeTxt)
        detalleNode.appendChild(codigoSecNode)        
        
        descripcionNode = rootNode.createElement('descripcion')
        descripcionNodeTxt = rootNode.createTextNode(deta.product_id.product_name)
        descripcionNode.appendChild(descripcionNodeTxt)
        detalleNode.appendChild(descripcionNode)        
        
        cantidadNode = rootNode.createElement('cantidad')
        cantidadNodeTxt = rootNode.createTextNode(str(deta.quantity))
        cantidadNode.appendChild(cantidadNodeTxt)
        detalleNode.appendChild(cantidadNode)        
        
        precioUnitarioNode = rootNode.createElement('precioUnitario')
        precioUnitarioNodeTxt = rootNode.createTextNode(str(deta.unit_price))
        precioUnitarioNode.appendChild(precioUnitarioNodeTxt)
        detalleNode.appendChild(precioUnitarioNode)        
        
        descuentoNode = rootNode.createElement('descuento')
        descuentoNodeTxt = rootNode.createTextNode(str(deta.discount))
        descuentoNode.appendChild(descuentoNodeTxt)
        detalleNode.appendChild(descuentoNode)        
        
        precTotSinImpNode = rootNode.createElement('precioTotalSinImpuesto')
        precTotSinImpNodeTxt = rootNode.createTextNode(str(deta.total_price))
        precTotSinImpNode.appendChild(precTotSinImpNodeTxt)
        detalleNode.appendChild(precTotSinImpNode)

        #impuestos Node 
        impuestosNode = rootNode.createElement('impuestos')
        detallesNode.appendChild(impuestosNode)

        #impuesto Node 
        impuestoNode = rootNode.createElement('impuesto')
        impuestosNode.appendChild(impuestoNode)

        impuestoCodNode = rootNode.createElement('codigo')
        impuestoCodNodeTxt = rootNode.createTextNode(totalImpCod)
        impuestoCodNode.appendChild(impuestoCodNodeTxt)
        impuestoNode.appendChild(impuestoCodNode)

        impuestocodigoPorcentjeNode = rootNode.createElement('codigoPorcentaje')
        impuestocodigoPorcentjeNodeTxt = rootNode.createTextNode(totalImpTarifIva)
        impuestocodigoPorcentjeNode.appendChild(impuestocodigoPorcentjeNodeTxt)
        impuestoNode.appendChild(impuestocodigoPorcentjeNode)

        tipTarifDict = dict(mng_fact_properties.tipTarifIva)
        tipTarifRes = ''
        if tipTarifDict[totalImpTarifIva].find('%') > 0:
            tipTarifRes = tipTarifDict[totalImpTarifIva].replace('%','.00')
        else:
            tipTarifRes = tipTarifDict[totalImpTarifIva]

        impuestoTarifaNode = rootNode.createElement('tarifa')
        impuestoTarifaNodeTxt = rootNode.createTextNode(tipTarifRes)
        impuestoTarifaNode.appendChild(impuestoTarifaNodeTxt)
        impuestoNode.appendChild(impuestoTarifaNode)
        
        impuestoBaseImpNode = rootNode.createElement('baseImponible')
        impuestoBaseImpNodeTxt = rootNode.createTextNode(str(deta.total_price))
        impuestoBaseImpNode.appendChild(impuestoBaseImpNodeTxt)
        impuestoNode.appendChild(impuestoBaseImpNode)        
        
        impuestoValorNode = rootNode.createElement('valor')
        impuestoValorNodeTxt = rootNode.createTextNode(str(deta.total_price * int(float(tipTarifRes)) / 100))
        impuestoValorNode.appendChild(impuestoValorNodeTxt)
        impuestoNode.appendChild(impuestoValorNode)


    xml_str = rootNode.toprettyxml(indent ="\t") 
    
    save_path_file = "invElect/" + str(invoice.user.id) + invoice.Invoice_no_final + ".xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)
    
    return save_path_file


def GenClavAccMod11(clavAcc):
    factores = itertools.cycle((2,3,4,5,6,7))
    suma = 0
    for digito, factor in zip(reversed(clavAcc), factores):
        suma += int(digito)*factor
    control = 11 - suma%11
    if control == 10:
        return 1
    else:
        return control


#Opens up page as PDF Oder Page
class ViewPDF(View):
    
    def get(self,request,invoice_id, *args, **kwargs):
        
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            invoice = None
        
        prodListidsCat= []

        InvdetailAct = InvoiceDetail.objects.filter(invoice_id=invoice_id)

        for invda in InvdetailAct:
            prodListidsCat.append(invda.product_id.mngProductCategory_id.id)

        #categories = MngProductCategory.objects.all()
        categories = MngProductCategory.objects.filter(id__in=prodListidsCat)

        context = {  
            'invoice': invoice,
            'invdetail': InvdetailAct,
            'categories': categories,
        }

        pdf = render_to_pdf('invoices/pdf/invoiceOrder.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

#Fact Elect
class DownloadXML(View):
    def get(self, request,invoice_id, *args, **kwargs):
        print('esta aqui')
        xml = createFactElectXml(invoice_id)
        print(xml)
        # response = HttpResponse(xml, content_type='application/xml')
        # #filename = "Invoice_%s.xml" %("12341231")
        # content = "attachment; filename='%s'" %(xml)
        # response['Content-Disposition'] = content
        # return response
        return redirect('newInvoiceDetail',  invoice_id=invoice_id)

class Xades(object):

    def sign(self, xml_document, file_pk12, password):
        """
        Metodo que aplica la firma digital al XML
        TODO: Revisar return
        """
        xml_str = xml_document.encode('utf-8')
        JAR_PATH = 'firma/firmaXadesBes.jar'
        JAVA_CMD = 'java'
        firma_path = os.path.join(os.path.dirname(__file__), JAR_PATH)
        command = [
            JAVA_CMD,
            '-jar',
            firma_path,
            xml_str,
            base64.b64encode(file_pk12),
            base64.b64encode(password)
        ]
        try:
            logging.info('Probando comando de firma digital')
            subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            output = e.output
            logging.error('Llamada a proceso JAVA codigo: %s' % returncode)
            logging.error('Error: %s' % output)

        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        res = p.communicate()
        return res[0]