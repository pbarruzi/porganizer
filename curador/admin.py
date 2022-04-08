from django.contrib import admin

from .models import Especialidade, CuradorEspecialidade

class EspecialidadeAdmin(admin.ModelAdmin):

    # selecionar quais campos participam da lista
    list_display = (
        'titulo',
    )
    
    list_filter = (
    )

class CuradorEspecialidadeAdmin(admin.ModelAdmin):

    # selecionar quais campos participam da lista
    list_display = (
        'curador',
        'especialidade',
    )
    
    list_filter = (
        'curador',
        'especialidade',
    )

admin.site.register(Especialidade, EspecialidadeAdmin)
admin.site.register(CuradorEspecialidade, CuradorEspecialidadeAdmin)
