from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    CustomUserAdmin class for customizing the admin interface for the CustomUser model.

    This class extends Django's built-in UserAdmin to adjust the displayed fields,
    search functionality, and ordering of users in the admin panel. It also sets up
    the fieldsets for adding and modifying users.
    """
    model = CustomUser

    # defines the layout of the forms for viewing and editing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    # defines the layout of the form for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    # specifies the columns to display in the list view of users
    list_display = ['email', 'is_staff', 'is_active']

    # enables searching for users by their email
    search_fields = ('email',)

    # specifies the default ordering of the user list (by email)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
