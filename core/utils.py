from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.models import AutomaticEmail


def forgot_password_email(user, email, request):
    auto_email = AutomaticEmail.objects \
        .get(type=AutomaticEmail.FORGOT_PASSWORD)

    # gera token e uid para URL
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    url_kwargs = {'token': token, 'uidb64': uid}
    url = reverse('account:password_reset_confirm', kwargs=url_kwargs)

    # prefixos do request HTTP
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = 'https' if request.is_secure() else 'http'
    protocol += '://'

    # monta token URL do form de reset de senha
    password_token_url = protocol + domain + url

    # formata email
    conteudo = {'password_token_url': password_token_url}
    assunto = auto_email.get_subject()
    corpo = auto_email.get_formatted_text(conteudo)
    corpo_html = auto_email.get_formatted_html(conteudo)

    auto_email.send_email(
        assunto, corpo, corpo_html, settings.EMAIL_HOST_USER, email
    )
