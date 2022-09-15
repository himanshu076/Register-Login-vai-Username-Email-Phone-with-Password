from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from accounts.models import User

# Register your models here.
@admin.register(User)
class UserAdminModel(UserAdmin):

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "username",
                "roll", "age", "gender", "phone_number")}),
        (_("Profile"), {"fields": ("profile_pic", "bio")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    readonly_fields = ["date_joined"]

    list_display = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name', "is_staff")
    # list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    # search_fields = ("first_name", "last_name", "email")
    ordering = ("-date_joined",)
    # filter_horizontal = (
    #     "groups",
    #     "user_permissions",
    # )
