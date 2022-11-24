from invoices.models import Invoice
from management.models import MngFactElect
from accounts.models import Account
from datetime import datetime
from xml.dom import minidom
from datetime import datetime
import itertools

class XmlBuildFactElect():

    def create(self,invoice_id):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            invoice = None

        Invdetail = getAllActualInvoiceDetails(invoice)

        mng_fact_properties = MngFactElect.objects.get(is_active=True)
        mainAccnt = Account.objects.get(is_superadmin=True)

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
        estab = '001'  # Creo que establecimiento
        ptoEmi = '001'  # Creo que punto de emision
        numSec = str(invoice.Invoice_no).zfill(9)
        codNum = numSec[1:]
        tipEmi = mng_fact_properties.tipoEmision
        tipIdentCompr = invoice.billing_customer_id.mngDocumentType_id.description
        flagGuiaRemis = False
        guiaRem = ''
        if flagGuiaRemis:
            guiaRem = '001-001-000000001'  # Ejemplo de Guia de Remision
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

        # totalConImpuestos Node
        totalConImpNode = rootNode.createElement('totalConImpuestos')
        factNode.appendChild(totalConImpNode)

        # totalImpuesto Node
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

        # detalles Node
        detallesNode = rootNode.createElement('detalles')
        factNode.appendChild(detallesNode)

        for deta in Invdetail:

            # detalle Node
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

            # impuestos Node
            impuestosNode = rootNode.createElement('impuestos')
            detallesNode.appendChild(impuestosNode)

            # impuesto Node
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
                tipTarifRes = tipTarifDict[totalImpTarifIva].replace('%', '.00')
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

        xml_str = rootNode.toprettyxml(indent="\t")

        save_path_file = "invElect/" + str(invoice.user.id) + invoice.Invoice_no_final + ".xml"

        with open(save_path_file, "w") as f:
            f.write(xml_str)

        return save_path_file

    
def GenClavAccMod11(clavAcc):
    factores = itertools.cycle((2, 3, 4, 5, 6, 7))
    suma = 0
    for digito, factor in zip(reversed(clavAcc), factores):
        suma += int(digito) * factor
    control = 11 - suma % 11
    if control == 10:
        return 1
    else:
        return control

def getAllActualInvoiceDetails(invoice):
    return invoice.invoicedetail_set.all()

