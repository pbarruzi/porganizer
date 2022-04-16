from django.apps import apps
from django.core.mail import send_mail
from django.db import models
from django.utils.decorators import classonlymethod
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError

from string import Formatter
from time import sleep


SIM = 'S'
NAO = 'N'
PADRAO = 'P'

BOOLEAN_CHOICES = (
    (False, _('Não')),
    (True, _('Sim')),
)

SIM_NAO_CHOICES = (
    (SIM, _('Sim')),
    (NAO, _('Não')),
)

SIM_NAO_PADRAO_CHOICES = (
    (SIM, _('Sim')),
    (NAO, _('Não')),
    (PADRAO, _('Padrão')),
)


def float_zero_ou_positivo(value):
    if value < 0:
        raise ValidationError(_(
            'O valor deve ser maior ou igual a zero!'
        ))


class Configuracao(models.Model):
    """
    Configurações especiais do Curador
    """
    appointments_to_pay = models.PositiveSmallIntegerField(
        verbose_name=_('Atendimentos para ser Pago'),
        help_text=_('Número de Atendimentos para que o Curador\
                    passe a ser Pago'),
        null=True,
    )
    average_to_pay = models.FloatField(
        verbose_name=_('Nota média para ser Pago'),
        help_text=_('Nota média nos Atendimentos, para que o Curador\
                    passe a ser Pago'),
        null=True,
    )

    class Meta:
        verbose_name = _('Config do Curador')
        verbose_name_plural = _('Config do Curador')

    def __str__(self):
        return '{}:{}'.format(
            self.appointments_to_pay, self.average_to_pay
        )


class AutomaticEmail(models.Model):
    """
    Registro de conteúdo default de e-mails automáticos enviados pelo sistema.

    Utilize get_formatted_text() para formatar as tags do texto do e-mail.
    """
    # choices
    FORGOT_PASSWORD = 1
    CURADOR_HAS_NEW_CLIENT = 10

    EMAIL_TYPE_CHOICES = (
        (FORGOT_PASSWORD, _('Nova Senha')),
        (CURADOR_HAS_NEW_CLIENT, _('Curador tem um novo Cliente')),
    )

    # campos
    type = models.PositiveSmallIntegerField(
        verbose_name=_('Tipo de E-mail'),
        help_text=_(
            'Determina do tipo de e-mail  '
            'que este registro representa.'
        ),
        choices=EMAIL_TYPE_CHOICES,
        unique=True,
        default=FORGOT_PASSWORD,
    )
    subject = models.CharField(
        max_length=60,
        verbose_name=_('E-mail Subject'),
    )
    text = models.TextField(
        verbose_name=_('E-mail Texto'),
        help_text=mark_safe(_(
            "Text which will be presented in the e-mail's body.<br/>"
            'Tags may be used to dynamically insert other '
            "content in the e-mail's body.<br/><br/>"
            'Tag list:<br/>'
            '- General:<br/>'
            '--- {user} (will insert an username of the client)<br/>'
            "--- {client_name} (will insert the client's full name)<br/>"
            "--- {client_email} (will insert the client's e-mail)<br/>"
            '--- {list_client_names} (will insert a list of all '
            'client names)<br/>'
            '--- {document_name} (will insert the name of the document '
            'evaluated)<br/>'
            '- Checklist Section Refused:<br/>'
            '--- {checklist_refused_section} (will insert the name of '
            'the checklist section that was refused)<br/>'
            '--- {checklist_refused_reason} (will insert the reason '
            'for checklist section being refused)<br/>'
            '- Password Changed by Admin & New Password:<br/>'
            '--- {password_token_url} (will insert the link to a form that '
            'allows the user to redefine his password)<br/>'
            '- Alerts:<br/>'
            '--- {section_label} (will insert the name of the '
            'section completed)<br/>'
            '--- {receipt_document_name} (will insert the name of the '
            'document which the client has sent a receipt of)<br/>'
            '--- {rating} (will insert the rating of the client as '
            'declared by compliance)<br/>'
            '--- {compliance_user} (will insert the name of the compliance '
            'user involved in the event, if any)<br/>'
            '--- {compliance_evaluation_reason} (will insert the reason for '
            'approval or refusal of the client as written by the compliance '
            'user)<br/>'
            '--- {document_status} (will insert the evaluation status of the '
            'document, approved or refused)<br/>'
            '--- {document_evaluation_reason} (will insert the reason for '
            'approval or refusal of the document as written by the '
            'compliance/sales user)<br/>'
            '--- {manager_section} (will insert the name of which section the '
            'client was approved/refused in by a manager)<br/>'
            '--- {manager_evaluation_reason} (will insert the reason of the '
            'approval/refusal as stated by the manager)<br/>'
            '--- {funds_value} (will insert the value in funds of the client '
            ' as inputted by the client services user)<br/>'
            '--- {funds_currency} (will insert the currency of the client as '
            'inputted by the client services user)<br/>'
            "--- {funds_info} (will insert any additional info of the "
            "client's funds as inputted by the client services user)<br/>"
            "--- {otc_pf_number} (will insert the client's OTC Portfolio "
            "Number)<br/>"
            "--- {mcm_inc_pf_number} (will insert the client's MCM Inc. "
            "Portfolio Number)<br/>"
            "--- {mcm_ltd_pf_number} (will insert the client's MCM Ltd. "
            "Portfolio Number)<br/>"
            "--- {dtvm_pf_number} (will insert the client's DTVM Portfolio "
            "Number)<br/>"
            "--- {credit_reason} (will insert the reason for approval/refusal "
            "of credit facility)<br/>"
            "--- {credit_im_value} (will insert the client's Initial Margin "
            "Credit Value)<br/>"
            "--- {credit_iv_value} (will insert the client's Variation Margin "
            "Credit Value)<br/>"
            "--- {client_desk} (will insert the desk the client has chosen "
            "to work with)<br/>"
            "--- {products_add_docs_list} (will insert the list of "
            "products/assets that the client has chosen which require "
            "additional documentation)<br/>"
            "- Additional Document Approval:<br/>"
            "--- {add_doc_product} (will insert the name of the product "
            "associated with the approved additional document)<br/>"
            "- Password Changing by Email:<br/>"
            "--- {email_password_changing_token} (will insert the token for "
            "password changing that will be sent by email to the client)<br/>"
            "- Revalidation by Email:<br/>"
            "--- {email_revalidation_token} (will insert the token for "
            "revalidation that will be sent by email to the client)<br/>"
            '<br/>'
            'Please make sure the tags are correct, and in the correct '
            'type of e-mail, as they may cause the e-mail body content '
            'to be incorrect if they are not.'
        )),
    )
    html = models.TextField(
        verbose_name=_('E-mail HTML Content'),
        help_text=mark_safe(_(
            "HTML Content which will be presented in the e-mail's body.<br/>"
            '<br/>'
            'Tags may be used to dynamically insert other content in the '
            "e-mail's body, and work exactly as they do in the above field."
        )),
        null=True,
        blank=True,
    )
    delay = models.FloatField(
        verbose_name=_('Delay entre emails'),
        help_text=_(
            'Define o intervalo de delay entre o '
            'envio de múltiplos emails deste tipo.'
        ),
        validators=[float_zero_ou_positivo],
        default=1,
    )

    class Meta:
        verbose_name = _('Configuraçao E-mail Automatico')
        verbose_name_plural = _("Configuraçao E-mails Automaticos")

    def __str__(self):
        return self.get_type_display()

    def get_formatter(self):
        if not hasattr(self, 'formatter'):
            self.formatter = EmailFormatter()

        return self.formatter

    def get_subject(self):
        """
        Retorna subject com prefixo especificado.
        """
        return 'Registri - ' + self.subject

    def get_formatted_text(self, content):
        """
        Retorna texto formatado com conteúdo recebido.
        """
        formatter = self.get_formatter()

        return formatter.format(self.text, **content)

    def get_formatted_html(self, content):
        """
        Retorna texto formatado com conteúdo recebido.
        """
        formatter = self.get_formatter()
        html = self.html or ''

        return formatter.format(html, **content)

    def send_email(self, assunto, corpo, corpo_html, host_email, target_email):
        # obs.: backend do gmail sempre usa EMAIL_HOST_USER como remetente
        sleep(self.delay)
        send_mail(
            assunto, corpo, host_email, [target_email],
            html_message=corpo_html
        )

# utils de models

class EmailFormatter(Formatter):
    """
    https://stackoverflow.com/a/20250018
    """

    def __init__(self, missing='', bad_fmt=''):
        self.missing, self.bad_fmt = missing, bad_fmt

    def get_field(self, field_name, args, kwargs):
        # handle a key not found
        try:
            val = super().get_field(field_name, args, kwargs)
        except (KeyError, AttributeError):
            val = None, field_name

        return val

    def format_field(self, value, spec):
        # handle an invalid format
        if value is None:
            return self.missing

        try:
            return super().format_field(value, spec)
        except ValueError:
            if self.bad_fmt is not None:
                return self.bad_fmt
            else:
                raise
