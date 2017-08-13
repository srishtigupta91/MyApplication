import datetime
import pytz
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from promo.models import VoucherCode
from django.forms.extras.widgets import *

class DrawForm(forms.ModelForm):
    sex_blank_choice = (('', 'Lad or Lady ?'),)
    age_gp_blank_choice = (('', "Born in 70's?"),)
    terms = forms.BooleanField(label="I agree to the TNC", initial=True)
    sex = forms.ChoiceField(choices=sex_blank_choice + VoucherCode.GENDER , label="sex", initial='', widget=forms.Select())
    age_gp = forms.ChoiceField(choices=age_gp_blank_choice + VoucherCode.age_choices, widget=forms.Select())
    first_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder':'First Name','class':'placeholder_design'}))
    email_address = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'Email Address','class':'placeholder_design'}))
    phone_number = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder':'Mobile Number','class':'placeholder_design'}))
    class Meta:
        model = VoucherCode
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'Code','class':'placeholder_design'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Last Name','class':'placeholder_design'})
        }
        fields = ('code', 'store', 'first_name', 'last_name', 'phone_number', 'email_address', 'sex', 'age_gp', 'terms')

    def __init__(self, *args, **kwargs):
        super(DrawForm, self).__init__(*args, **kwargs)
        self.fields['store'].empty_label = "Store Purchased"

    def clean(self):
        code = self.cleaned_data.get("code", "")
        if VoucherCode.objects.filter(code__iexact=code, used=False).exists():
            self.cleaned_data['code'] = VoucherCode.objects.get(code__iexact=code)
            return self.cleaned_data
        raise forms.ValidationError("Invalid Coupon Code")
