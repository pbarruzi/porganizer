from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_summernote.admin import SummernoteModelAdmin

from account.models import User
from .models import (
    SiteConfig,
    TextoSite,
    ClienteSetup,
)


class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Imagens'), {
            'fields': (
                'logo_image', 'logo_company_image', 'logo_book',
                'bg_general_image', 'bg_landing_image',
                'favicon_image',
            ),
        }),
        ('CSS', {
            'fields': ('css_file', )
        }),
    )

    def has_add_permission(self, request, obj=None):
        return False if SiteConfig.objects.exists() else True

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class TextoSiteAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'landing_page_wellcome_text',
        'login_wellcome_msg',
    )

    fieldsets = (
        (_('Língua'), {
            'fields': (
                'language',
            ),
        }),
        ('Wellcome Landing Page', {
            'fields': (
                'landing_page_wellcome_phrase',
                'landing_page_wellcome_text',
                'landing_page_join_us',
            )
        }),
        ('Wellcome Login Page', {
            'fields': (
                'login_wellcome',
                'login_wellcome_msg',
            )
        }),
    )
    
    def has_add_permission(self, request, obj=None):
        return False if SiteConfig.objects.exists() else True

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(TextoSite, TextoSiteAdmin)
