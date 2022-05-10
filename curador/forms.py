from django.forms import ModelForm
from atendimento import models as atendimento_models

class EncerrarAtendimentoForm(ModelForm):
    class Meta:
        model = atendimento_models.Atendimento
        fields = ['anotacoes_curador',]