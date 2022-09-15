from tkinter.messagebox import NO
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from account.managers import CustomUserManager
from account.choice import UserRoll


# password = admin@123

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email_address'), unique=True, blank=True)
    # phone = models.CharField(_('phone_number'), max_length=12,)
    roll = models.CharField(max_length=2, choices=UserRoll.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    place = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                    related_name='profile')
    user_pic = models.ImageField(upload_to='static/image/%Y/%m/%d')

