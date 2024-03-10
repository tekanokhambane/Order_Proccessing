from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Admin, Staff, Customer


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Define the fields to be displayed in the Django admin interface
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    # Define the fields that can be filtered in the Django admin interface
    list_filter = ("is_staff", "is_superuser", "is_active")
    # Define the fields that can be searched in the Django admin interface
    search_fields = ("email", "first_name", "last_name")
    # Define the fieldsets for the Django admin interface
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "username")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
    )
    # Define the fields that will be shown when creating a new user from the Django admin interface
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )
    # Define the ordering of users in the Django admin interface
    ordering = ("email",)
    # Define the field used to log in
    # Note: 'email' is set as the USERNAME_FIELD in the User model
    USERNAME_FIELD = "email"

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return queryset
    #     return queryset.filter(is_staff=False)


admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Customer)
