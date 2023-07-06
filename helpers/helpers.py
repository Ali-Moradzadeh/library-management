CUSTOMER = 'Customer'
ADMIN = 'Admin'

RELATED_PROFILE = { 
    ADMIN: 'AdminProfile',
    CUSTOMER: 'CustomerProfile',
}

USER_ROLE_CHOICES = (
    (ADMIN, ADMIN),
    (CUSTOMER, CUSTOMER),
)

import re
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if len(value)==11 and re.fullmatch(r"^09[0-9]+", value):
        return value
    raise ValidationError("invalid phone number")

from functools import reduce


def validate_national_code(value):
    if not value:
        return value
    if len(value)!=10:
        raise ValidationError("national code must be exactly 10 digits. if your national code starts with some 0 please enter them.")
    if not value.isnumeric():
        raise ValidationError("national code must be numeric")
    
    ctrl_digit, nine_digit = int(value[-1]), value[:-1]
    remain = reduce(lambda a,b : a + (10 - b[0])*int(b[1]), enumerate(nine_digit), 0) % 11
    remain = remain if remain < 2 else 11 - remain

    if remain != ctrl_digit:
        raise ValidationError("Invalid national code.")
    return value


def validate_alpha_values(value):
    if (not value) or "".join(value.split(" ")).isalpha():
        return value
    raise ValidationError("This Field Accept No Numbers/Symbols")