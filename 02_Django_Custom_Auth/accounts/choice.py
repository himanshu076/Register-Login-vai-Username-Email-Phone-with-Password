from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoll(models.TextChoices):
    USER = 'U', _('User')
    VENDOR = 'V', _('Vendor')


class Gender(models.TextChoices):
    MALE = 'ML', _('Male')
    FEMALE = 'FL', _('Female')
    TRANSGENDER = 'TS', _('Transgender')
    OTHER = 'OT', _('Other')
