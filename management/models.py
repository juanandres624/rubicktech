from django.db import models

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

    def __str__(self):
        return self.description

class MngProductBrand(models.Model):
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

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

    tipoEmision = models.CharField(max_length=1, choices=tipEmision)
    tipoComprobante = models.CharField(max_length=2, choices=tipComprob)
    tipoAmbiente = models.CharField(max_length=1, choices=tipAmbient)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    # def __str__(self):
    #     return self.description