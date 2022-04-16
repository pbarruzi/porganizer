from django.forms import ModelForm
from atendimento import models

class AtendimentoForm(ModelForm):
    class Meta:
        model = models.Atendimento
        fields = ['curador']