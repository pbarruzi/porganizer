from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget

from atendimento import models as atendimento_models
from curador import models

class EncerrarAtendimentoForm(ModelForm):
    class Meta:
        model = atendimento_models.Atendimento
        fields = ['anotacoes_curador',]

class AboutMeForm(ModelForm):
    class Meta:
        model = models.CuradorAboutMe
        fields = ['titulo', 'descricao',]
        
        widgets = {
            # 'foo': SummernoteWidget(),
            'descricao': SummernoteWidget(),
        }        