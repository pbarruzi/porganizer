from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User,
)


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'user_picture')
        }),
        ('Informações Básicas', {
            'fields': (
                'name', 'last_login', 'user_type',
            )
        }),
        ('Permissões', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            )
        }),
    )

    list_display = [
        'username', 'name', 'email', 'user_type', 'is_active', 'is_staff',
        'date_joined',
    ]
    list_filter = ['user_type', 'is_active', 'is_staff', 'date_joined']
    search_fields = [
        'username', 'name', 'email', 'user_type', 'is_active', 'is_staff',
        'date_joined',
    ]


admin.site.register(User, UserAdmin)
