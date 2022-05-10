from django.db import models
from django.utils.translation import gettext_lazy as _

from account import models as models_account
from curador import models as models_curador

PENDING = 0
RUIM = 1
FRACO = 2
MEDIO = 3
BOM = 4
OTIMO = 5

ATENDIMENTO_CHOICES = (
    (PENDING,'Pendente.'),
    (RUIM,'Não Gostei.'),
    (FRACO,'Achei muito fraco.'),
    (MEDIO,'Razoável, ajudou pouca coisa.'),
    (BOM,'Achei bom, aprendi coisas importantes.'),
    (OTIMO,'Atendimento Ótimo! Transformador!'),
)

ABERTO = 0
ENCERRADO = 1

AGENDAMENTO_STATUS_CHOICES = (
    (ABERTO,'Agendamento Aberto'),
    (ENCERRADO,'Agendamento Encerrado'),
)


class Atendimento(models.Model):
    # Informações atendimentos
    #
    curador = models.ForeignKey(
        models_account.User,
        verbose_name=_('Curador'),
        on_delete=models.PROTECT,
        related_name='consultas_curador',
    )
    cliente = models.ForeignKey(
        models_account.User,
        verbose_name=_('Cliente'),
        related_name='consultas_cliente',
        on_delete=models.PROTECT,
    )
    avaliacao_cliente = models.SmallIntegerField(
        verbose_name=_('Avaliação do Cliente'),
        choices=ATENDIMENTO_CHOICES,
        default=PENDING,
    )
    depoimento_cliente = models.TextField(
        verbose_name=_('Depoimento do Cliente'),
        null=True,
        blank=True,
    )
    data_depoimento = models.DateField(
        verbose_name=_('Data do Depoimento'),
        help_text=_('(DD/MM/AAAA)'),
        null=True,
        blank=True,
    )
    data_agendamento = models.DateField(
        verbose_name=_('Data do Agendamento'),
        help_text=_('(DD/MM/AAAA)'),
        auto_now_add=True,
    )
    status_agendamento = models.SmallIntegerField(
        verbose_name=_('Status do Agendamento'),
        choices=AGENDAMENTO_STATUS_CHOICES,
        default=ABERTO,
    )
    anotacoes_curador = models.TextField(
        verbose_name=_('Anotações do Curador para acompanhamento'),
        null=True,
        blank=True,
    )
    data_encerramento = models.DateField(
        verbose_name=_('Data do Enceramento'),
        help_text=_('(DD/MM/AAAA)'),
        null=True,
        blank=True,
    )
    
    class Meta:
        verbose_name = _('Atendimento')
        verbose_name_plural = _('Atendimentos')

    def __str__(self):
        curador = getattr(self, 'curador', None)
        cliente = getattr(self, 'cliente', None)
        return 'Curador: {}, Cliente: {}, Nota: {}'.format(
            getattr(curador, 'name', ''),
            getattr(cliente, 'name', ''),
            self.avaliacao_cliente,
        )

    @property
    def avaliou_curador(self):
        score = None
        
        try:
            qs = self.cliente\
                .userrating_set\
                .filter(rating__object_id=self.curador_id)\
                .first()
            if qs:
                score = qs.score
        except:
            pass
        return score