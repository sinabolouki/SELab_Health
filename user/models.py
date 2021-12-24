import datetime

import django
from django.core.exceptions import ValidationError
from django.db import models


def validate_digit_length(national_code):
    if not (national_code.isdigit() and len(national_code) == 10):
        raise ValidationError('%(phone)s must be 10 digits', params={'phone': national_code}, )


class User(models.Model):
    name = models.CharField(max_length=128)
    national_code = models.CharField(max_length=10, validators=[validate_digit_length], unique=True)
    password = models.CharField(max_length=128)
    isAdmin = models.BooleanField(default=False)
    isDoctor = models.BooleanField(default=False)
    token = models.CharField(max_length=256, default="")
    token_exp_time = models.DateTimeField(default=django.utils.timezone.now)
    bio = models.CharField(max_length=128, default='bio')
    sign_up_date = models.DateTimeField(auto_now_add=True)
