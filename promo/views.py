import random
import json
import code128
import os
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.views.generic import FormView
from django.utils import timezone
from django.conf import settings

from promo.forms import DrawForm
from promo.models import VoucherCode, BarCodes, Config
from django.http import HttpResponse

class VoucherFormView(FormView):
    model = VoucherCode
    template_name = 'form.html'
    form_class = DrawForm

    def form_valid(self, form):
        voucher_code = form.cleaned_data['code']
        voucher_code.first_name = form.cleaned_data['first_name']
        voucher_code.last_name = form.cleaned_data['last_name']
        voucher_code.email_address = form.cleaned_data['email_address']
        voucher_code.phone_number = form.cleaned_data['phone_number']
        voucher_code.store = form.cleaned_data['store']
        voucher_code.claimed = timezone.now()
        voucher_code.sex = form.cleaned_data['sex']
        voucher_code.age_gp = form.cleaned_data['age_gp']
        voucher_code.news_letter = form.cleaned_data.get('news_letter', False)
        voucher_code.terms = form.cleaned_data['terms']
        voucher_code.used = True
        voucher_code.save()

        today = timezone.now()
        bar_code = BarCodes.objects.filter(used=False, valid_from__lte=today, valid_till__gte=today).first()
        if bar_code:
            bar_code.code = voucher_code
            bar_code.assign_date = timezone.now()
            bar_code.used = True
            bar_code.save()
            data = Config.objects.first()
            return render(self.request, 'thanks.html', {'code': bar_code.bar_code, 'config':data,'valid_till':bar_code.valid_till})

        else:
            return render(self.request, 'thanks.html', {'no_bar_code': True})

def SendEmail(request):
    if request.method == "GET":
        bar_code = request.GET.get('bar_code')
        code128.image(bar_code).save(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/static/svg/" + bar_code + ".png")
        bar_code = BarCodes.objects.filter(bar_code=bar_code, code__isnull=False)[0]
        ctx = {
            'message': 'success',
            'code' : bar_code.bar_code,
            'server_name':settings.SERVER_NAME,
            'valid_till':bar_code.valid_till,
                }
        message = render_to_string('email.html', ctx)
        email_message = EmailMessage(
            "Coupon Details", message, settings.DEFAULT_FROM_EMAIL, [bar_code.code.email_address])
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=True)
        return HttpResponse(json.dumps({'msg': 'sucess'}), content_type="application/json")


