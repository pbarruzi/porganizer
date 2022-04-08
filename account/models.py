import re
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.core import validators

ADMINISTRADOR = 0     # Administrador do sistema. Admin
STAFF = 1             # Compliance do sistema. Tarefas auxiliares ao Admin
CURADOR = 4           # Profissional que faz atendimento à consulentes
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
                user_type=User.CURADOR,
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
                user_type=User.CLIENTE,
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
        default=STAFF,
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
    cliente = ClienteAtivoManager()

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return self.name or self.username

    @property
    def qtde_atendimentos_curador(self):
        """
        Retorna a quantidade de atendimentos do curador.
        """

        if self.user_type != CURADOR:
            return 0

        return 10

    @property
    def qtde_atendimentos_cliente(self):
        """
        Retorna a quantidade de atendimentos do cliente.
        """

        if self.user_type != CLIENTE:
            return 0

        return 20
