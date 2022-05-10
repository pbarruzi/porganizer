from django.urls import path, reverse_lazy, re_path

from curador import views

app_name = 'curador'

urlpatterns = [
    # assim que entra, é direcionado para a "views.home" que faz o roteamento
    # para a tela adequada
    
    # curadores
        path(
        'curador/dashboard/',
        views.CuradorDashboardView.as_view(),
        name='dashboard'
    ),
        path(
        'curador/encerrar/<int:pk>/atendimento',
        views.CuradorEncerrarAtendimentoView.as_view(),
        name='encerrar-atendimento'
    ),

]