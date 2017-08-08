from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        if is_superuser:
            extra_fields['is_active'] = is_superuser
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    MALE = '1'
    FEMALE = '2'
    GENDER = (
        (MALE, _("Male")),
        (FEMALE, _("Female"))
    )

    ADMIN = '1'
    ADVERTISER = '2'
    USER = '3'
    ROLE = (
        (ADMIN, _("ADMIN")),
        (ADVERTISER, _("ADVERTISER")),
        (USER, _("USER")),
    )

    email = models.EmailField(_('Email address'), max_length=254, unique=True)
    name = models.CharField(_('Name'), max_length=30, null=True, blank=True)
    screen_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_block = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    dob = models.DateField(null=True, blank=True)
    last_active = models.DateField(auto_now=True)
    gender = models.CharField(
        verbose_name=_("select gender."),
        max_length=1,
        choices=GENDER
    )
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    role = models.CharField(choices=ROLE, max_length=2)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        app_label = _('accounts')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    @property
    def age(self):
        current_time = timezone.now()
        if self.dob:
            age = current_time.year - self.dob.year
            return age

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
