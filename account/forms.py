from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from django import forms

from .models import (
    User, CLIENTE
)
from core.utils import forgot_password_email

class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'name', 'email',
            'user_picture'
        ]


class UserAdministradorCreationForm(UserCreationForm):
    """
    Cadastro de usuários Admin do Sistema.
    Usuário Admin somente serão criados pelo manager
    Possui todos os privilégios de administração do sistema
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'name', 'email', 'user_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.ADMINISTRADOR
        if commit:
            user.save()
        return user


class UserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        PerfilUsuario = apps.get_model('site_setup', 'PerfilUsuario')
        self.fields['user_type'].choices = PerfilUsuario.get_choices()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
            'is_active',
            'is_staff',
            'user_picture',
        ]


class UserGenericCreationForm(UserCreationForm):
    """
    Cadastro comum a todos os tipos de usuários que chegam pelo site
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username', 'name', 'email',
        ]

    @transaction.atomic
    def save(self, commit=True):
        """
        Regras para tipo de usuário:
        - VEIO PELO SITE --> user_type = CLIENTE;
        """
        user = super().save(commit=False)
        user.user_type = CLIENTE
        user.save()
        return user


class RegistriPasswordResetForm(forms.Form):
    username = forms.CharField(
        label=_('Username'),
        required=False,
    )
    email = forms.EmailField(
        label=_('E-mail'),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email', None)

        if not email:
            raise ValidationError(
                _('Por favor, preencha o campo.'),
                code='no_input'
            )

    def save(self, request=None):
        email = self.cleaned_data["email"]

        email_sent = False

        for user in self.get_users(email):
            if not email:
                email = user.get_email
            forgot_password_email(user, email, request)
            email_sent = True

        return email_sent

    def get_users(self, email):
        # query do método original
        users = User.objects.filter(email__iexact=email, is_active=True)

        """
        # query extra caso não tenha obtido resultado
        if not users.exists():
            username = self.cleaned_data['username']
            users = User.objects \
                .filter(username__iexact=username, is_active=True)
        """

        return (u for u in users if u.has_usable_password())

