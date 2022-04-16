"""
SITE_MEDIA = '__site__/'
IMAGENS = 'img/'
BACKGROUND_IMAGE = SITE_MEDIA + IMAGENS + 'bg/'
LOGO_IMAGE = SITE_MEDIA + IMAGENS + 'logo/'
FAVICON_IMAGE = SITE_MEDIA + IMAGENS + 'favicon/'
"""
from django.conf import settings


def site_logo_path(self, filename):
    # file will be uploaded to MEDIA_ROOT
    return settings.LOGO_IMAGE + '_{0}'.format(filename)


def site_background_path(self, filename):
    # file will be uploaded to MEDIA_ROOT
    return settings.BACKGROUND_IMAGE + '_{0}'.format(
        filename)


def landing_background_path(self, filename):
    # não apagar
    return settings.LANDING_BG_IMAGE + '_{0}'.format(
        filename)


def site_favicon_path(self, filename):
    # file will be uploaded to MEDIA_ROOT
    return settings.FAVICON_IMAGE + '_{0}'.format(
        filename)


def site_css_path(self, filename):
    # file will be uploaded to MEDIA_ROOT
    return settings.CSS_PATH + '_{0}'.format(
        filename)
