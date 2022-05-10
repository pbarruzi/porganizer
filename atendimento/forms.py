from django.forms import ModelForm
from atendimento import models

class AtendimentoAvalForm(ModelForm):
    class Meta:
        model = models.Atendimento
        fields = ['depoimento_cliente',]