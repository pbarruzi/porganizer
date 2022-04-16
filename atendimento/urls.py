from django.urls import path, reverse_lazy, re_path

from atendimento import views

app_name = 'agendamento'

urlpatterns = [
    # assim que entra, é direcionado para a "views.home" que faz o roteamento
    # para a tela adequada

    path(
        'cliente/dashboard/',
        views.AtendimentoDashboardView.as_view(),
        name='cliente-dashboard'
    ),
    path(
        'cliente/contratar/<int:curador_id>/curador/free',
        views.AtendimentoContratarFreeView.as_view(),
        name='cliente-contratar-free'
    ),
    path(
        'cliente/contratar/<int:curador_id>/curador/remunerado',
        views.AtendimentoContratarRemuneradoView.as_view(),
        name='cliente-contratar-remunerado'
    ),
    path(
        'json-contratar/curador/',
        views.JasonContratarCuradorView.as_view(),
        name='json-contratar-curador',
    ),


]