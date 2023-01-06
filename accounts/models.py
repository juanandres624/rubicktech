from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class myAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None):

        if not username:
            raise ValueError('Nombre de Usuario Requerido')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = False
        user.save(using = self._db)

        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user

class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length = 50, null = False, blank = True)
    last_name       = models.CharField(max_length = 50, null = False, blank = True)
    username        = models.CharField(max_length = 50, null = False, blank = True, unique = True)
    email           = models.EmailField(max_length = 100, null = True, blank = True)
    phone_number    = models.CharField(max_length = 50, null = False, blank = True)
    numRuc          = models.CharField(max_length = 13, null = True, blank = True)
    razSocial       = models.CharField(max_length = 150, null = True, blank = True)
    nombCom         = models.CharField(max_length = 150, null = True, blank = True)
    dirMatr         = models.CharField(max_length = 255, null = True, blank = True)
    dirEstablec     = models.CharField(max_length = 255, null = True, blank = True)
    obligContab     = models.BooleanField(default = False)
    contribEspec    = models.CharField(max_length = 13, null = True, blank = True)
    admin_id        = models.CharField(max_length = 255, null = False, blank = True)

    #required
    date_joined     = models.DateTimeField(auto_now_add = True, null = False, blank = True)
    last_login      = models.DateTimeField(auto_now_add = True, null = False, blank = True)
    is_admin        = models.BooleanField(default = False)
    is_staff        = models.BooleanField(default = False)
    is_active       = models.BooleanField(default = False)
    is_superadmin   = models.BooleanField(default = False)

    date_added = models.DateField(auto_now_add=True)


    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS  = ['first_name','last_name']

    objects = myAccountManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    # def __str__(self):
    #     return self.email

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
