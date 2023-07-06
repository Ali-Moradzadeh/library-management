from django.contrib.auth.models import BaseUserManager
import django.contrib.auth.password_validation as validators
from django.utils import timezone
from helpers import helpers


class UserManager(BaseUserManager):
    def _prepare_user(self, username, phone_number, password, email="", **kwargs):
        user = self.model(
            username=username,
            phone_number=phone_number,
            email=email,
            last_login=timezone.now(),
        )
        validators.validate_password(user=user, password=password)
        user.set_password(password)
        return user

    def create_admin(self, username, phone_number, password, email=""):
        user = self._prepare_user(username=username, phone_number=phone_number, password=password, email=email)
        user.role = helpers.ADMIN
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_customer(self, username, phone_number, password, email=""):
        user = self._prepare_user(username=username, phone_number=phone_number, password=password, email=email)
        user.role = helpers.CUSTOMER
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password, email=""):
        user = self._prepare_user(username=username, phone_number=phone_number, password=password, email=email)
        
        user.role = helpers.ADMIN
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def create_user(self, username, phone_number, password, email=""):
        return self.create_customer(username=username, phone_number=phone_number, password=password, email=email)


class CustomerManager(BaseUserManager):
    def get_queryset(self):
        return self.model.objects.filter(role=helpers.CUSTOMER)


class StaffManager(BaseUserManager):
    def get_queryset(self):
        return self.model.objects.filter(is_staff=True)