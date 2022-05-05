import re
from django.db import models
from django.db.models import Count, Avg
from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.core import validators
from core import models as core_models

ADMINISTRADOR = 0  # Administrador do sistema. Admin
STAFF = 1          # Compliance do sistema. Tarefas auxiliares ao Admin
CURADOR = 4        # Profissional que faz atendimento à consulentes
CLIENTE = 5        # Pessoa que se cadastra no sistema e marca uma consulta


class CuradorAtivoManager(models.Manager):
    """
    Retorna apenas as Linhas com curadores Ativos
    para a visão dos clientes
    """
    def get_queryset(self):
        return super()\
            .get_queryset()\
            .filter(
                user_type=CURADOR,
                is_active=True,
            )


class ClienteAtivoManager(models.Manager):
    """
    Retorna apenas as Linhas com Cliente Ativos
    para a visão dos clientes
    """
    def get_queryset(self):
        return super()\
            .get_queryset()\
            .filter(
                user_type=CLIENTE,
                is_active=True,
            )


class User(AbstractBaseUser, PermissionsMixin):
    """
    Usuário do sistema. O modelo utilizado é o de SUBSTITUIÇÃO
    onde o cadastro de User do Django é SUBSTITUIDO por um outro.
    UserManager - para assumir as features do User, createsuperuser por exemplo
    PermissionsMixin,, para manter o máximo de compatibilidade com o admin
    
    Usuários possíveis:
        a. admin
        b. staff
        c. curador
        d. consulente
    """

    USER_TYPE_CHOICES = (
        (STAFF, _('Administrativo')),
        (CURADOR, _('Curador')),
        (CLIENTE, _('Cliente')),
    )

    username = models.CharField(
        _('Usuário'),
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _(
                    'Informe um nome de usuário válido. '
                    'Este valor deve conter apenas letras, números '
                    'e os caracteres: @/./+/-/_ .'
                ),
                'invalid'
            )
        ],
    )
    name = models.CharField(
        _('Nome Completo'),
        max_length=100,
        blank=True
    )
    email = models.EmailField(
        # também pode ser utilizado como login
        'E-mail',
        unique=True
    )
    is_staff = models.BooleanField(
        _('Equipe'),
        default=False
    )
    is_active = models.BooleanField(
        _('Ativo'),
        default=True
    )
    user_type = models.PositiveSmallIntegerField(
        _('Tipo usuário'),
        choices=USER_TYPE_CHOICES,
        default=CLIENTE,
    )
    user_picture = models.ImageField(
        _('Imagem'),
        upload_to='users_pictures',
        blank=True,
        null=True,
    )
    date_joined = models.DateTimeField(
        _('Data de Registro'),
        auto_now_add=True
    )

    # o Django vai precisar das configurações abaixo em alguns momentos
    # um deles é na criação do superusuário. Estes são os campos que ele pede.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    curadores = CuradorAtivoManager()
    clientes = ClienteAtivoManager()

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return self.name or self.username

    @property
    def curador_estatisticas(self):
        """
        Retorna as estatísticas de atendimentos do curador:
            - curador - pk do curador
            - qt - quantidade total de atendimentos do curador
            - media - nota média dada pelos clientes
        """
        statis = {'curador': self.pk, 'qt': 0, 'media': 0.0}
        
        if self.user_type != CURADOR:
            return statis

        if not hasattr(self, 'consultas_curador'):
            return statis
        
        atendimento_qs = self.consultas_curador.all()
        statis_qs = atendimento_qs.values('curador',)\
            .annotate(
                qt=Count('curador'),
                media=Avg('avaliacao_cliente'),
            )
            
        return statis_qs[0] if statis_qs else statis

    @property
    def curador_status_atendimentos(self):
        """
        Retorna os status de atendimentos do curador:
            - curador - pk do curador
            - 0 - quantidade de atendimediamentos em aberto
            - 1 - quantidade de atendimentos encerrados
        """
        status = [{'curador': 3, 'status_agendamento': 0, 'qt': 0}, {'curador': 3, 'status_agendamento': 1, 'qt': 0}]
        
        if self.user_type != CURADOR:
            return status

        if not hasattr(self, 'consultas_curador'):
            return status
        
        atendimento_qs = self.consultas_curador.all()
        status = atendimento_qs.values('curador','status_agendamento')\
            .annotate(
                qt=Count('status_agendamento'),
            )
        return status

    @property
    def curador_remunerado(self):
        """
        Retorna se o curador é Remunerado ou Gratuíto
        A partir de um certo número de atendimento e
        de uma certa média de avaliação, o curador entra
        na faixa de Remunerado. Abaixo disto ele está na faixa de
        gratuíto.
        As bases estão definidas em core.config
        """

        if self.user_type != CURADOR:
            return False

        config = core_models.Configuracao.objects.first()
        
        if not config:
            return False

        stats = self.curador_estatisticas
        qt = stats.get('qt', 0)
        media = stats.get('media', 0.0)
        
        if config.appointments_to_pay > qt:
            return False
        
        if config.average_to_pay > media:
            return False
        
        return True
