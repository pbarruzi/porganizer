from django.urls import path, reverse_lazy, re_path

from django.contrib.auth.views import LogoutView
from account import views

app_name = 'account'

urlpatterns = [
    # assim que entra, é direcionado para a "views.home" que faz o roteamento
    # para a tela adequada

    path('logado/', views.home, name='home'),
    path('deslogado/', views.LogoutView.as_view(), name='logout_system'),

    # login / logout
    path('login/', views.RegistriLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(
        next_page=reverse_lazy('account:logout_system')), name='logout'),

    # FORGOT PASSWORD: BEGIN
    path(
        'forgot-password/',
        views.ForgotPasswordFormView.as_view(),
        name='forgot-password'
    ),
    path(
        'reset-password/<uidb64>/<token>/',
        views.ResetPasswordFormView.as_view(),
        name='password_reset_confirm'
    ),
    # FORGOT PASSWORD: END

    # CRIAÇÃO GENERICA DE USUÁRIOS
    path(
        'registrar/cliente/',
        views.UserCreateView.as_view(),
        name='registrar-cliente'
    ),

    # UPDATE DE USUÁRIOS
    path(
        'alterar/user/',
        views.UserUpdateView.as_view(),
        name='alterar_usuario'
    ),
]