from django.db import models

class MngDocumentType(models.Model):
    docType = (
        ('Cedula Identidad', 'Cedula Identidad'), ('RUC', 'RUC'), ('Pasaporte', 'Pasaporte'),
    )

    description = models.CharField(max_length=20, choices=docType)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description

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
        ("Active", 'Active'), ('Inactive', 'Inactive'),
    )

    description = models.CharField(max_length=20, choices=statusType)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description