from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from . import models
from helpers import helpers


@transaction.atomic
def test_integrity(test_obj, obj1, obj2, *fields):
    for field in fields:
        field = field.field.name
        v1 = getattr(obj1, field)
        v2 = getattr(obj2, field)
        
        try:
            with transaction.atomic():
                setattr(obj2, field, v1)
                obj2.save()
            test_obj.fail(f'Duplicate {field} allowed.')
        except IntegrityError:
            setattr(obj2, field, v2)
            obj2.save()


def test_unvalids(test_obj, obj, field, *unvalid_datas):
    field = field.field.name
    for unvalid in unvalid_datas:
        with test_obj.assertRaises(ValidationError):
            v = getattr(obj, field)
            setattr(obj, field, unvalid)
            obj.save()
        setattr(obj, field, v)
        obj.save()


class UserModelTest(TestCase):
    def setUp(self):
        self.count = models.User.objects.count
        self.users_kwargs = {
            "user_1": {
                "username": "test_user",
                "phone_number": "09123456789",
                "email": "test_user@gmail.com",
                "password": "Ali541379"
            },
            "user_2": {
                "username": "test_user2",
                "phone_number": "09222222222",
                "email": "test_user2@gmail.com",
                "password": "Ali541379"
            }
        }
    
    def get_related_creation_method(self, role):
        mapped = {
            helpers.ADMIN: models.User.objects.create_admin,
            helpers.CUSTOMER: models.User.objects.create_customer,
        }
        return mapped.get(role, None)
    
    def common_user_attributes_test(self, role, key):
        creation_method = self.get_related_creation_method(role)
        kv = self.users_kwargs[key]
        usr = creation_method(**kv)
        
        # attributes test
        self.assertEqual(usr.username, kv["username"])
        self.assertEqual(usr.phone_number, kv["phone_number"])
        self.assertEqual(usr.email, kv["email"])
        self.assertTrue(usr.check_password("Ali541379"))
        self.assertEqual(self.count(), 1)
        
        #test: unvalid data for phone_number
        unvalids = ["091234567899", "0912123", "0912345s789", "08123456789",]
        test_unvalids(self, usr, models.User.phone_number, *unvalids)
        
        #signals test for creating profile
        prf = models.AdminProfile.objects.filter(user=usr)
        self.assertTrue(prf.exists())
        prf = prf[0]
        prf.first_name = "test user first"
        prf.last_name = "test user last"
        prf.national_code = "0000000000"
        prf.save()
        self.assertEqual(prf.first_name, "test user first")
        self.assertEqual(prf.last_name, "test user last")
        self.assertEqual(prf.national_code, "0000000000")
        
        unvalids = ["0000000", "0000000000000", "00000e0000", "2652842845"]
        test_unvalids(self, prf, models.AdminProfile.national_code, *unvalids)
        
        #integrity test
        integrity_usr = models.User(**self.users_kwargs["user_2"])
        mdl = models.User
        fields = [mdl.username, mdl.phone_number, mdl.email]
        test_integrity(self, usr, integrity_usr, *fields)
    
        #delete test
        self.assertEqual(type(integrity_usr.delete()), tuple)
        self.assertEqual(self.count(), 1)
        
        return usr
    
    def test_create_delete_admin(self):
        usr = self.common_user_attributes_test(helpers.ADMIN, "user_1")
        # attributes test
        self.assertTrue(usr.is_staff)
        self.assertEqual(usr.role, helpers.ADMIN)
        
        # deleting test
        self.assertEqual(type(usr.delete()), tuple)
        self.assertEqual(self.count(), 0)
    
    def test_create_delete_customer(self):
        usr = self.get_related_creation_method(helpers.CUSTOMER)(**self.users_kwargs["user_1"])
        # attributes test
        self.assertFalse(usr.is_staff)
        self.assertEqual(usr.role, helpers.CUSTOMER)
