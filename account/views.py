from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, PasswordResetConfirmView, PasswordResetView,
)

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.translation import activate
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, FormView, View,
)
from django.contrib.auth.forms import AuthenticationForm
from .models import (User, ADMINISTRADOR, CURADOR, CLIENTE, STAFF)
from .forms import (
    UserAdminCreationForm, RegistriPasswordResetForm
)


class RegistriAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = 254


class RegistriLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = RegistriAuthenticationForm

    # GET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['placeholder_username'] = _('Entre com sua conta ou e-mail')
        context['placeholder_password'] = _('Senha')
        return context

    # POST

    def form_valid(self, form):
        redirect = super().form_valid(form)
        LANGUAGE_SESSION_KEY = 'pt-br'
        # seta linguagem para sessão
        user = self.request.user
        user_language = 'pt-br'
        activate(user_language)
        self.request.session[LANGUAGE_SESSION_KEY] = user_language
        return redirect

    def form_invalid(self, form):
        redirect = super().form_invalid(form)
        return redirect


class LogoutView(View):
    def get(self, request):
        return render(request, 'core/index.html')


def home(request):
    """
    Após o login o usuário é redirecionado para esta view e ela
    Define para qual Home (index) o usuário será redirecionado.
    """
    user = request.user

    if user.is_authenticated:
        if user.user_type == ADMINISTRADOR:
            return redirect('account:index_administrador')
        elif user.user_type == STAFF:
            return redirect('compliance:dashboard')
        elif user.user_type == CURADOR:
            return redirect('curador:dashboard')
        elif user.user_type == CLIENTE:
            return redirect('agendamento:atendimento-dashboard')

    return render(request, 'core/index.html')


def user_update(request):
    """
    Define qual view fará a alteração do usuário corrente
    """
    if request.user.is_authenticated:
        if request.user.user_type == User.ADMINISTRADOR:
            return redirect('account:alterar_administrador')
        elif request.user.user_type == User.STAFF:
            return redirect('account:alterar_staff')
        elif request.user.user_type == User.INVESTIDOR:
            return redirect('account:alterar_investidor')

    return render(request, 'core/index.html')


class UserTypeView(CreateView):
    """
    View que permite ao usuário escolher o seu papel no sistema
    """

    template_name = 'account/user_type_creation.html'
    form_class = UserAdminCreationForm

    # reverse_lazy() para resolver esta url mais tarde e
    # nao logo no momento da carga do sistema.
    success_url = reverse_lazy('account:index')


class UserCreateView(CreateView):
    """
    View de criação do usuário Visitante
    """

    model = User
    template_name = 'account/create-user.html'
    form_class = UserAdminCreationForm

    # reverse_lazy() para resolver esta url mais tarde e
    # nao logo no momento da carga do sistema.
    success_url = reverse_lazy('account:home')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Alterar dados do usuário.
    Está view é disponivel para o usuário e não
    para o back-office da empresa.
    """
    model = User
    template_name = 'account/user/alterar-dados.html'
    fields = ['name', 'email']
    success_url = reverse_lazy('account:home')

    def get_object(self):
        """
        devolve o objeto do usuário que será alterado.
        ele já está no contexto self.request
        """
        return self.request.user


class UserUpdatePasswordView(LoginRequiredMixin, FormView):
    """
    Aqui vamos utilizar o FormView, pois não  será utilizado
    o Model User diretamente.
    """
    template_name = 'account/user_update_password.html'
    success_url = reverse_lazy('core:index')

    # o Django já tem um form pronto para a alteração da senha:
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        """
        O construtor do PasswordChangeForm (__init__() ) precisa
        conhecer quem é o usuário. Então, temos que informar.

        Vamos fazer isto nos argumentos nomeados: kwargs
        """

        # pegar o kwargs principal e juntar o user nele.
        kwargs = super(UserUpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Aqui, acontece realmente a atualização do banco de dados
        """
        form.save()
        return super(UserUpdatePasswordView, self).form_valid(form)


# Forgoten password
class ForgotPasswordFormView(PasswordResetView):
    template_name = 'account/forgot-password.html'
    success_url = reverse_lazy('account:login')
    email_template_name = 'account/password_reset_email.html'
    form_class = RegistriPasswordResetForm

    def form_valid(self, form):
        email_sent = form.save(request=self.request)

        mensagem = _(
            'Caso o seu e-mail esteja correto, em breve você receberá um '
            'e-mail para a troca de senha.<br/><br/>'
            'Caso não tenha recebido o e-mail, por favor, verifique sua '
            'caixa de spam.'
        )
        
        mensagem = mark_safe(mensagem)
        if email_sent:
            # para algum futuro tratamento
            messages.info(self.request, mensagem)
        else:
            # para algum futuro tratamento quando não existir
            # nem e-mail nem usuario
            messages.info(self.request, mensagem)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print('invalid')


class ResetPasswordFormView(PasswordResetConfirmView):
    template_name = 'account/reset-password.html'
    success_url = reverse_lazy('account:login')

    # override no método da view original, método idêntico exceto
    # pelo redirecionamento em caso de token inválido
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        INTERNAL_RESET_URL_TOKEN = 'set-password'
        INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session \
                    .get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path \
                        .replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # redireciona em caso de token expirado
        msg = _('Este link para redefinição de senha expirou.')
        messages.warning(self.request, msg)
        return HttpResponseRedirect(reverse_lazy('account:login'))

    def form_valid(self, form):
        redirect = super().form_valid(form)

        now = timezone.now()

        obj = User.objects.get(pk=self.user.pk)
        obj.data_revalidacao = now
        obj.data_revalidacao_email = now
        obj.save()

        msg = _('Senha modificada com sucesso!')
        messages.info(self.request, msg)

        return redirect
