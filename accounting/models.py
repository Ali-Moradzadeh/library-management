from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django_jalali.db import models as jmodels
import jdatetime
from helpers import helpers, file_handlers
from validators import validate_file_extension
from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=11, unique=True, validators=[helpers.validate_phone_number])
    email = models.EmailField(unique=True, null=True, blank=True)
    role = models.CharField(choices=helpers.USER_ROLE_CHOICES, max_length=12)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = jmodels.jDateField(default=jdatetime.date.today())

    objects = managers.UserManager()
    staffs = managers.StaffManager()
    customers = managers.CustomerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'email']
    
    def clean(self):
        flds = list(filter(lambda i: i.validators, self._meta.fields))
        for fld in flds:
            for vld in fld.validators:
                vld(getattr(self, fld.name))
    
    def save(self, *args, **kwargs):
        self.clean()
        self.is_staff = self.is_admin
        if self.is_customer:
            self.is_superuser = False
        self.is_staff |= self.is_superuser
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username} - {self.phone_number} - {self.get_role_display()} - {self.id}'
    
    @property
    def is_admin(self):
        return self.role == helpers.ADMIN

    @property
    def is_customer(self):
        return self.role == helpers.CUSTOMER

    def get_profile(self):
        profile_model_class = apps.get_model(
            'accounting', helpers.RELATED_PROFILE.get(self.role)
        )
        profile = profile_model_class.objects.get_or_create(user=self)[0]

        return profile


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(null=True, blank=True, max_length=132, validators=[helpers.validate_alpha_values])
    last_name = models.CharField(null=True, blank=True, max_length=132, validators=[helpers.validate_alpha_values])
    national_code = models.CharField(null=True, blank=True, max_length=10, unique=True, validators=[helpers.validate_national_code])
    image = models.FileField(upload_to=file_handlers.custom_file_handler, blank=True, null=True,
        validators=[validate_file_extension])
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def clean(self):
        helpers.validate_national_code(self.national_code)
        helpers.validate_alpha_values(self.first_name)
        helpers.validate_alpha_values(self.last_name)
    
    def save(self, *args, **kwargs):
        self.clean()
        if self.first_name:
            self.first_name = self.first_name.capitalize()
        if self.last_name:
            self.last_name = self.last_name.capitalize()
        
        super().save(*args, **kwargs)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.first_name}-{self.last_name}-{self.user.username}-{self.id}'


class AdminProfile(UserProfile):
    pass


class CustomerProfile(UserProfile):
    pass
