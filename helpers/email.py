import traceback

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import loader
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class EmailMixin(object):
    token_generator = default_token_generator
    subject_template_name = None
    plain_body_template_name = None
    html_body_template_name = None

    def create_email(self, user):
        assert self.plain_body_template_name or self.html_body_template_name
        context = self.get_email_context(user)
        subject = loader.render_to_string(self.subject_template_name, context)
        subject = ''.join(subject.splitlines())
        user_email=[user.email]

        if self.plain_body_template_name:
            plain_body = loader.render_to_string(
                self.plain_body_template_name, context)
            email_message = EmailMultiAlternatives(
                subject, plain_body, settings.DEFAULT_FROM_EMAIL, user_email)
        else:
            html_body = loader.render_to_string(
                self.html_body_template_name, context)
            email_message = EmailMessage(
                subject, html_body, settings.DEFAULT_FROM_EMAIL, user_email)
            email_message.content_subtype = 'html'
        return email_message

    def get_email_context(self, user):
        raise NotImplementedError("email context not define")


    def send_email(self, user):
        email_msg = self.create_email(user)
        try:
            email_msg.send(fail_silently=True)
        except Exception as e:
            print(traceback.format_exc(e))
