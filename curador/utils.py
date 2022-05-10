from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.models import AutomaticEmail


def curador_has_new_cliente(curador, cliente):
    """
        Envia um e-mail para o curador, logo após ele ser
    contratado por um cliente.

    Args:
        curador (_type_): account.User()
        cliente (_type_): account.User()
    
    Tags: espera por duas tags, que caso existam, serão preenchidas:
        . client_name:  Nome completo do cliente contratante
        . client_email: e-mail do cliente
    """
    auto_email = AutomaticEmail.objects \
        .get(type=AutomaticEmail.CURADOR_HAS_NEW_CLIENT)

    # formata email
    
    conteudo = {
        'client_name': cliente.name,
        'client_email': cliente.email,
    }
    assunto = auto_email.get_subject()
    corpo = auto_email.get_formatted_text(conteudo)
    corpo_html = auto_email.get_formatted_html(conteudo)

    auto_email.send_email(
        assunto, corpo, corpo_html, settings.EMAIL_HOST_USER, curador.email
    )


def curador_ended_session(curador, cliente):
    """
        Envia um e-mail para o cliente, logo após o curador 
        encerrar

    Args:
        curador (_type_): account.User()
        cliente (_type_): account.User()
    
    Tags: espera por duas tags, que caso existam, serão preenchidas:
        . client_name:  Nome completo do cliente contratante
        . curador_name: nome do Curador
    """
    auto_email = AutomaticEmail.objects \
        .get(type=AutomaticEmail.CURADOR_ENDED_SESSION)

    # formata email
    
    conteudo = {
        'client_name': cliente.name,
        'curador_name': curador.name,
    }
    assunto = auto_email.get_subject()
    corpo = auto_email.get_formatted_text(conteudo)
    corpo_html = auto_email.get_formatted_html(conteudo)

    auto_email.send_email(
        assunto, corpo, corpo_html, settings.EMAIL_HOST_USER, cliente.email
    )
