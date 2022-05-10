from django.urls import path, reverse_lazy, re_path

from atendimento import views

app_name = 'agendamento'

urlpatterns = [
    # assim que entra, é direcionado para a "views.home" que faz o roteamento
    # para a tela adequada

    path(
        'atendimento/dashboard/',
        views.AtendimentoDashboardView.as_view(),
        name='atendimento-dashboard'
    ),

    # clientes    
    path(
        'cliente/contratar/<int:curador_id>/curador',
        views.ClienteContratarCuradorView.as_view(),
        name='cliente-contratar-curador'
    ),
    path(
        'cliente/avaliar/<int:pk>/atendimento',
        views.ClienteAvaliarCuradorView.as_view(),
        name='cliente-avaliar-curador'
    ),
    path(
        'cliente/dashboard/',
        views.ClienteDashboardView.as_view(),
        name='cliente-dashboard'
    ),
    
    # curadores
        path(
        'curador/dashboard/',
        views.CuradorDashboardView.as_view(),
        name='curador-dashboard'
    ),

    # curadores não remunerados
    path(
        'curador/free/list',
        views.CuradoresFreeListView.as_view(),
        name='curador-free-list'
    ),
    path(
        'cliente/contratar/<int:curador_id>/curador/free',
        views.AtendimentoContratarFreeView.as_view(),
        name='cliente-contratar-free'
    ),
    
    # curadores remunerados
    path(
        'curador/remunerado/list',
        views.CuradoresRemuneradosListView.as_view(),
        name='curador-remunerado-list'
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