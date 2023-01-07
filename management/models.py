from django.db import models
from accounts.models import Account

class MngDocumentType(models.Model):
    docType = (
        ('05', 'CÉDULA'), ('04', 'RUC'), ('06', 'PASAPORTE'),('07', 'VENTA A CONSUMIDOR FINAL'),('08', 'IDENTIFICACIÓN DEL EXTERIOR'),
    )

    description = models.CharField(max_length=20, choices=docType)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.get_description_display()

class MngPersonType(models.Model):
    PersonType = (
        ('Natural', 'Natural'), ('Juridica', 'Juridica'),
    )

    description = models.CharField(max_length=20, choices=PersonType)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description

class MngCity(models.Model):
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description

class MngProductCategory(models.Model):
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,related_name= 'created_by_m_mngpc')

    def __str__(self):
        return self.description

class MngProductBrand(models.Model):
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,related_name= 'created_by_m_mngpb')

    def __str__(self):
        return self.description

class MngValues(models.Model):
    description = models.CharField(max_length=100)
    value = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description

class MngStatus(models.Model):
    statusType = (
        ("Activo", 'Activo'), ('Inactivo', 'Inactivo'), ('En Progreso', 'En Progreso'),('Completado', 'Completado'),
    )

    description = models.CharField(max_length=20, choices=statusType)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description

class MngPaymentType(models.Model):
    payType = (
        ('01', 'SIN UTILIZACION DEL SISTEMA FINANCIERO'), 
        ('15', 'COMPENSACIÓN DE DEUDAS'), 
        ('16', 'TARJETA DE DÉBITO'),
        ('17', 'DINERO ELECTRÓNICO'),
        ('18', 'TARJETA PREPAGO'),
        ('19', 'TARJETA DE CRÉDITO'),
        ('20', 'OTROS CON UTILIZACIÓN DEL SISTEMA FINANCIERO'),
        ('21', 'ENDOSO DE TÍTULOS'),
    )

    description = models.CharField(max_length=100, choices=payType)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.get_description_display()

class MngFactElect(models.Model):
    tipEmision = (
        ("1", 'Emisión normal'), 
    )
    tipComprob = (
        ("01", 'Factura'), 
        ("03", 'LIQUIDACIÓN DE COMPRA DE BIENES Y PRESTACIÓN DE SERVICIOS'), 
        ("04", 'NOTA DE CRÉDITO '), 
        ("05", 'NOTA DE DÉBITO'), 
        ("06", 'GUÍA DE REMISIÓN'), 
        ("07", 'COMPROBANTE DE RETENCIÓN'), 
    )
    tipAmbient = (
        ("1", 'Pruebas '),
        ("2", 'Producción'), 
    )
    tipCodImp = (
        ("2", 'IVA '),
        ("3", 'ICE'),
        ("5", 'IRBPNR'),
    )
    tipTarifIva = (
        ("0", '0% '),
        ("2", '12%'),
        ("3", '14%'),
        ("6", 'No Objeto de Impuesto'),
        ("7", 'Exento de IVA'),
        ("8", 'IVA diferenciado'),
    )

    tipoEmision = models.CharField(max_length=1, choices=tipEmision)
    tipoComprobante = models.CharField(max_length=2, choices=tipComprob)
    tipoAmbiente = models.CharField(max_length=1, choices=tipAmbient)
    codImp = models.CharField(max_length=1, choices=tipCodImp)
    tarifIva = models.CharField(max_length=1, choices=tipTarifIva)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    # def __str__(self):
    #     return self.description