from django.conf import settings
from django.utils.translation import (get_language)

from .models import SiteConfig, TextoSite


def site_settings(request):
    """
    Retorna imagens, texto e CSS do site conforme configurado no admin.
    """
    context = {}

    config = SiteConfig.objects.first()
    if config:
        context['bg_general_image'] = config.bg_general_image.name
        context['bg_landing_image'] = config.bg_landing_image.name
        context['logo_image'] = config.logo_image.name
        context['logo_company'] = config.logo_company_image.name
        context['favicon_image'] = config.favicon_image.name
        context['site_styles'] = config.css_file

    lang_code = get_language()
    text = TextoSite.objects.filter(language=lang_code).first()
    if text:
        context['landing_page_wellcome_phrase'] = text.landing_page_wellcome_phrase
        context['landing_page_wellcome_text'] = text.landing_page_wellcome_text
        context['landing_page_join_us'] = text.landing_page_join_us
        context['login_wellcome'] = text.login_wellcome
        context['login_wellcome_msg'] = text.login_wellcome_msg

    return context


def client_bg_img(request):
    context = {
        'CLIENT_BG_IMG': 'media/img/bg/bg_cli_logado.png'
    }

    return context
