from django.db import models
from django.utils.translation import gettext_lazy as _
from account import models as models_account


class Especialidade(models.Model):
    """
    Informações sobre especialidades que um curador pode atuar
    """
    titulo = models.CharField(
        verbose_name=_('Titulo da Especialidade'),
        max_length=100,
        null=True,
    )
    descricao = models.TextField(
        verbose_name=_('Descrição da Especialidade'),
        null=True,
    )

    class Meta:
        verbose_name = _('Especialidade de Consulta')
        verbose_name_plural = _('Especialidades de Consultas')

    def __str__(self):
        return '{}'.format(
            self.titulo,
        )


class CuradorEspecialidade(models.Model):
    """
    Link entre um curador e suas especialidades
    """
    curador = models.ForeignKey(
        models_account.User,
        on_delete=models.PROTECT,
        verbose_name=_('Curador'),
        related_name='curador_especialidades',
    )
    especialidade = models.ForeignKey(
        Especialidade,
        on_delete=models.PROTECT,
        verbose_name=_('Especialidade'),
        related_name='especialidade_curadores',
    )

    class Meta:
        verbose_name = _('Especialidade do Curador')
        verbose_name_plural = _('Especialidades do Curador')

    def __str__(self):
        return '{}-{}'.format(
            self.curador,
            self.especialidade.titulo,
        )
