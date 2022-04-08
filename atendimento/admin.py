from django.contrib import admin

from .models import Atendimento

class AtendimentoAdmin(admin.ModelAdmin):

    # selecionar quais campos participam da lista
    list_display = (
        'curador',
        'cliente',
        'avaliacao_cliente',
        'data_agendamento',
        'status_agendamento',
    )
    
    list_filter = (
        'curador',
        'curador__especialidade',
    )

admin.site.register(Atendimento, AtendimentoAdmin)
