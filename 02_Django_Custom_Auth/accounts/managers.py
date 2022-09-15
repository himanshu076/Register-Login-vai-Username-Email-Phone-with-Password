from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from core.utils import randomString


class UserManager(BaseUserManager):
    def _create_user(self, first_name, last_name, password, is_staff, is_superuser, username=None, email=None, phone_number=None, **kwargs):
        """
        CustomUser Manager for loging vai email or phone.
        """

        now = timezone.now()

        if not first_name:
            raise ValueError("You must enter a first name")

        if not last_name:
            raise ValueError("You must enter a last name")

        if not password:
            raise ValueError("You must enter a password")

        # Creates an username from email if doesn't exists
        if username is None:
            fname = str(first_name).lower().replace(' ', '')
            lname = str(last_name).lower().replace(' ', '')
            username = ''.join([fname, lname, randomString()])

        print('Your username is ', username)

        email = self.normalize_email(email)

        user = self.model(username = username,
                        first_name=first_name,
                        last_name=last_name,
                        is_staff = is_staff,
                        is_active = True,
                        is_superuser = is_superuser,
                        last_login = str(now),
                        date_joined = now,

                        email = email,
                        phone_number = phone_number,

                        **kwargs)

        user.set_password(password)
        user.save(using=self.db)

        return user

    # Creates a normal user
    def create_user(self, first_name, last_name, username=None, email=None, phone_number=None, password=None, **kwargs):
        return self._create_user(first_name, last_name, password, False, False, username, email, phone_number, **kwargs)

    # Creates a superuser
    def create_superuser(self, first_name, last_name, username=None, email=None, phone_number=None, password=None, **kwargs):
        return self._create_user(first_name, last_name, password, True, True, username, email, phone_number, **kwargs)


