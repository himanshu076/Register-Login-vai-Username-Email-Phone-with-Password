from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, AbstractUser)
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.choice import UserRoll, Gender
from core.utils import avatar_upload_location
from accounts.managers import UserManager


# Custom User Model Class
class User(AbstractBaseUser, PermissionsMixin):

  first_name = models.CharField(max_length=240)
  last_name = models.CharField(max_length=240)

  username = models.CharField(max_length=254, unique=True)

  email = models.EmailField(blank=True, null=True)
  # phone_number = PhoneNumberField(blank=True, null=True)
  phone_number = models.IntegerField(blank=True, null=True)
  roll = models.CharField(_('User_Roll'), max_length=2, choices=UserRoll.choices)

  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

  age = models.PositiveSmallIntegerField(blank=True, null=True)
  gender = models.CharField(max_length=5, choices=Gender.choices, blank=True, null=True)

  profile_pic = models.ImageField(blank=True, null=True, upload_to=avatar_upload_location)
  bio = models.CharField(max_length=512, blank=True, null=True)

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['first_name', 'last_name']
  EMAIL_FIELD = 'email'

  objects = UserManager()

  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')

  def __str__(self):
    return self.email

  def get_full_name(self):
    if self.first_name != '':
      return '%s %s' %(self.first_name, self.last_name)
    else:
      return self.username

  def get_short_name(self):
    return '%s' %(self.first_name)

  def get_absolute_url(self):
    pass

  def email_user(self, subject, message, from_email=None, **kwargs):
    send_mail(subject, message, from_email, [self.email], **kwargs)
