from django.db import models
from django.utils.translation import gettext_lazy as _
from core.crypto import encrypt, decrypt
from site_setup import tools_models


class SiteConfig(models.Model):
    # settings
    # imagens
    logo_image = models.ImageField(
        _('Imagem do Logo da Instituição'),
        upload_to=tools_models.site_logo_path,
        blank=True,
        null=True,
    )
    logo_company_image = models.ImageField(
        _('Company logo '),
        help_text='Imagem transparente, logo da empresa, que aparece, \
            por exemplo, na tela de login, do lado direito, ao alto, \
            sobre a bg_general_image. Transparente.',
        upload_to=tools_models.site_logo_path,
        blank=True,
        null=True,
    )
    logo_book = models.ImageField(
        _('Imagem do Logo da Instituição no Book'),
        upload_to=tools_models.site_logo_path,
        blank=True,
        null=True,
    )
    bg_general_image = models.ImageField(
        _('Imagem Geral de Background'),
        help_text='Imagem que aparece em background em várias partes do site',
        upload_to=tools_models.site_background_path,
        blank=True,
        null=True,
    )
    bg_landing_image = models.ImageField(
        _('Imagem Background Landing Page'),
        upload_to=tools_models.site_background_path,
        blank=True,
        null=True,
    )
    favicon_image = models.ImageField(
        _('Imagem do icon favorito'),
        help_text=_('Imagem que aparece em todas as telas. Icone da empresa'),
        upload_to=tools_models.site_favicon_path,
        blank=True,
        null=True,
    )

    # css
    css_file = models.FileField(
        _('Arquivo com o CSS'),
        upload_to=tools_models.site_css_path,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Configurações Gerais do Site')
        verbose_name_plural = _('Configurações Gerais do Site')

    def __str__(self):
        return str(_('Configurações Gerais'))


class TextoSite(models.Model):
    PORTUGUES = 'pt-br'
    INGLES = 'en'

    LANGUAGE_CHOICES = (
        (PORTUGUES, _('PORTUGUES')),
        (INGLES, _('INGLES')),
    )

    # Textos que o cliente minicom pode por no site
    language = models.CharField(
        verbose_name=_('Linguagem do texto'),
        max_length=5,
        default=PORTUGUES,
        choices=LANGUAGE_CHOICES,
        blank=True,
        unique=True,
    )
    landing_page_wellcome_phrase = models.CharField(
        verbose_name=_('Página de Entrada. Boas Vindas em uma Frase'),
        max_length=256,
        null=True,
        blank=True,
    )
    landing_page_wellcome_text = models.TextField(
        verbose_name=_('Página de Entrada. Boas Vindas em um Texto'),
        null=True,
        blank=True,
    )
    landing_page_join_us = models.CharField(
        verbose_name=_('Mensagem para "Junte-se a nós"'),
        max_length=128,
        null=True,
        blank=True,
    )
    login_wellcome = models.CharField(
        verbose_name=_('Página de login. Boas Vindas'),
        max_length=256,
        null=True,
        blank=True,
    )
    login_wellcome_msg = models.TextField(
        verbose_name=_('Página de login. Mensagem'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Texto Site')
        verbose_name_plural = _('Textos do Site')

    def __str__(self):
        return 'sys:{}'.format(
            self.language,
        )


class ClienteSetup(models.Model):
    # Mantido apenas por Minicom
    document_id = models.CharField(
        verbose_name=_('Identificação do Contratante'),
        help_text=_('Código interno gerado ao habilitar o contratante do sistema.\
                    Copiado ClienteContratante.Codigo_id'),
        max_length=30,
        null=True,
        blank=True,
    )
    data_setup = models.DateField(
        verbose_name=_('Data Setup'),
        null=True,
        blank=True,
    )
    last_check = models.DateField(
        verbose_name=_('Última Checagem'),
        help_text=_('Determina se o site está em dia e habilitado a funcionar'),
    )

    class Meta:
        verbose_name = _('Cliente Setup')

    def __str__(self):
        return 'sys:{}'.format(
            decrypt(self.document_id),
        )

    def save(self, *args, **kwargs):
        self.cnpj = encrypt(self.document_id)

    @property
    def is_registered(self):
        cnpj_by_cli = ClienteContratante.objects.only('document_id').first()
        return decrypt(self.document_id) == cnpj_by_cli.document_id


class ClienteContratante(models.Model):
    # Informações o cliente Contratante do Sistema
    nome = models.CharField(
        verbose_name=_('Nome do Cliente'),
        max_length=100,
        null=True,
        blank=True,
    )
    document_id = models.CharField(
        verbose_name=_('CNPJ/CPF/TAX ID'),
        help_text=_('Documento que identifica exclusivamente o Contratante'),
        max_length=30,
        null=True,
        blank=True,
    )
    endereco = models.CharField(
        verbose_name=_('Endereço completo'),
        max_length=256,
        null=True,
        blank=True,
    )
    telefone = models.CharField(
        verbose_name=_('Telefone'),
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Cliente Contratante')
        verbose_name_plural = _('Cliente Contratante')

    def __str__(self):
        return 'sys:{}'.format(
            self.nome,
        )
