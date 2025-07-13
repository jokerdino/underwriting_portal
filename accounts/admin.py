# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username",
        "ro_code",
        "oo_code",
        "user_type",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "user_type")
    search_fields = ("username", "ro_code", "oo_code")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Codes", {"fields": ("ro_code", "oo_code")}),
        (
            "Roles & Type",
            {"fields": ("user_type", "reset_password", "last_login")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
