from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoll(models.TextChoices):
    USER = 'U', _('User')
    VENDOR = 'V', _('Vendor')