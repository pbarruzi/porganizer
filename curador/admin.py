from django.contrib import admin
from curador import models
from django_summernote.admin import SummernoteModelAdmin


class AboutMeAdmin(SummernoteModelAdmin):

    Summernote_fields = ['descricao']
    # selecionar quais campos participam da lista
    list_display = (
        'descricao',
    )
    
    list_filter = (
    )


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

admin.site.register(models.CuradorAboutMe, AboutMeAdmin)
admin.site.register(models.Especialidade, EspecialidadeAdmin)
admin.site.register(models.CuradorEspecialidade, CuradorEspecialidadeAdmin)
