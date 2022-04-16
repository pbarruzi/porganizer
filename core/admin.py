from django.contrib import admin

from .models import AutomaticEmail, Configuracao


class ConfiguracaoAdmin(admin.ModelAdmin):

    # Configurações para os curadores
    list_display = (
        'appointments_to_pay',
        'average_to_pay'
    )
    
    list_filter = (
    )


class AutomaticEmailAdmin(admin.ModelAdmin):

    # selecionar quais campos participam da lista
    list_display = (
        'type',
        'subject',
    )
    
    list_filter = (
    )

admin.site.register(AutomaticEmail, AutomaticEmailAdmin)
admin.site.register(Configuracao, ConfiguracaoAdmin)
