from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Store(models.Model):
    country = models.ForeignKey('promo.Country')
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class VoucherCode(models.Model):
    age_choices = ((1,'1980 - 2017 - "Feeling fresh I bet"'),
                   (2, '1970 - 1979 - "We knew it"'),
                   (3, '1900 - 1969 - "Looking good though"'),)

    FEMALE = "LADY"
    MALE = "LAD"

    GENDER = (
        (MALE, "Lad"),
        (FEMALE, "Lady")
    )

    code = models.CharField(max_length=256, unique=True)
    store = models.ForeignKey('promo.Store',null=True,blank=True)
    first_name = models.CharField(max_length=256,null=True,blank=True)
    last_name = models.CharField(max_length=256,null=True,blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    email_address = models.EmailField(max_length=256, null=True, blank=True)
    sex = models.CharField(max_length=32,choices=GENDER, null=True, blank=True)
    age_gp = models.IntegerField(choices=age_choices,null=True,blank=True, default=0)
    created = models.DateTimeField(auto_now=True)
    claimed = models.DateTimeField(null=True, blank=True)
    terms = models.BooleanField(default=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return 'Voucher<%s %s>'%(self.id,self.used)

    def store_name(self):
        return self.store.name


class BarCodes(models.Model):
    code = models.ForeignKey(VoucherCode, null=True, blank=True)
    bar_code = models.CharField(max_length=255, unique=True)
    used = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_till = models.DateTimeField()
    assign_date = models.DateField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'BarCode<%s %s %s>'%(self.id,self.code,self.bar_code)

    def promo_code(self):
        return self.code


class Config(models.Model):
    fb_link = models.CharField(max_length=255)
    date = models.DateField()
