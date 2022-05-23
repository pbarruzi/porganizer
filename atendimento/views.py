from datetime import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views.generic import (View, TemplateView,)
from django.views.generic.edit import (UpdateView)
from django.db import transaction
from django.urls import reverse_lazy


from atendimento import models
from atendimento.models import ABERTO, ENCERRADO
from account import models as account_models
from atendimento.forms import AtendimentoAvalForm
from curador import utils as curador_utils

class AtendimentoDashboardView(TemplateView):
    template_name = 'atendimento/atendimento-index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        remunerados = [ user for user in account_models.User.curadores.all() if user.curador_remunerado]
        nao_remunerados = [ user for user in account_models.User.curadores.all() if not user.curador_remunerado]

        # context['atendimentos_correntes'] = atendimentos_correntes
        # context['atendimentos_passados'] = atendimentos_passados
        context['remunerados'] = remunerados
        context['nao_remunerados'] = nao_remunerados
        return context


# curadores free
class CuradoresFreeListView(TemplateView):
    template_name = 'atendimento/curadores-free-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        free = [ user for user in account_models.User.curadores.all() if not user.curador_remunerado]
        context['nao_remunerados'] = free
        context['SIZE'] = len(free)
        return context

class AtendimentoContratarFreeView(TemplateView):
    template_name = 'atendimento/cliente-contratar-free.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        curador_id = kwargs.get('curador_id')
        if curador_id:
            curador = account_models.User.objects\
                .filter(pk=curador_id)\
                .first()
            context['curador'] = curador
            
        return context


# Curadores Remunerados
class CuradoresRemuneradosListView(TemplateView):
    template_name = 'atendimento/curadores-remunerados-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        remunerados = [ user for user in account_models.User.curadores.all() if user.curador_remunerado]
        context['remunerados'] = remunerados
        context['SIZE'] = len(remunerados)
    
        return context

class AtendimentoContratarRemuneradoView(TemplateView):
    template_name = 'atendimento/cliente-contratar-remunerado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        curador_id = kwargs.get('curador_id')
        if curador_id:
            curador = account_models.User.objects\
                .filter(pk=curador_id)\
                .first()
            context['curador'] = curador
            
        return context

# Clientes

class ClienteDashboardView(TemplateView):
    template_name = 'atendimento/cliente-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        atendimentos_correntes = models.Atendimento.objects.filter(
            cliente=user,
            status_agendamento=ABERTO,
        ).order_by('curador')

        atendimentos_passados = models.Atendimento.objects.filter(
            cliente=user,
            status_agendamento=ENCERRADO,
        ).order_by('curador')

        context['atendimentos_correntes'] = atendimentos_correntes
        context['atendimentos_passados'] = atendimentos_passados
        return context


class ClienteContratarCuradorView(TemplateView):
    template_name = 'atendimento/cliente-contratar-curador.html'
    success_url = reverse_lazy('agendamento:cliente-dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        curador_id = kwargs.get('curador_id')
        if curador_id:
            curador = account_models.User.objects\
                .filter(pk=curador_id)\
                .first()
            context['curador'] = curador
            
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = self.request.user
        curador_id = kwargs.get('curador_id')
        
        if not curador_id:
            msg = 'Curador não identificado (ID)'
            messages.warning(self.request, msg)
            return HttpResponseRedirect(self.success_url)
    
        curador = account_models.User.objects\
            .filter(pk=curador_id)\
            .first()

        if not curador:
            msg = 'Curador não Cadastrado em nosso Banco de Dados'
            messages.warning(self.request, msg)
            return HttpResponseRedirect(self.success_url)
    
        has_obj = models.Atendimento\
            .objects\
            .filter(
                curador=curador,
                cliente=user,
            )\
            .first()
        
        if has_obj:
            msg = 'Você já está com uma sessão em aberto com {}. Obrigado.'.format(curador)
            messages.info(request, msg)
            return HttpResponseRedirect(self.success_url)

            
        contrato = models.Atendimento()
        contrato.curador = curador
        contrato.cliente = user
        try:
            contrato.save()
            msg = 'Olá {}, você e {} firmaram um compromisso. Desejamos sucesso!'\
                .format(user, curador)
            messages.success(request, msg)

            msg = 'Em breve {} entrará em contato, aguarde.'.format(curador)
            messages.info(request, msg)
            
            curador_utils.curador_has_new_cliente(curador, user)
            
        except ValueError as e:
            msg = 'Infelizmente algo saiu errado {}.\n\
                Por favor informe nosso time, obrigado'.format(e)
            messages.warning(request, msg)
        
        return HttpResponseRedirect(self.success_url)


class ClienteAvaliarCuradorView(UpdateView):
    template_name = 'atendimento/cliente-avaliar-curador.html'
    success_url = reverse_lazy('agendamento:cliente-dashboard')
    # form_class = AtendimentoAvalForm
    model = models.Atendimento
    fields = ['depoimento_cliente']

    def form_valid(self, form):
        form.instance.data_depoimento = datetime.now()
        form.save()
        return super().form_valid(form)
        

# curador
class CuradorDashboardView(TemplateView):
    template_name = 'atendimento/curador-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        atendimentos_correntes = models.Atendimento.objects.filter(
            cliente=user,
            status_agendamento=ABERTO,
        ).order_by('curador')
        context['atendimentos_correntes'] = atendimentos_correntes
        return context
 
# Json's

class JasonContratarCuradorView(View):
    """
    Realiza o link de contrato entre o usuario e o curador 
    escolhido (remunerado ou free).
    """

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        response = {'mensagem': 'Contratação realizada com sucesso'}
        user = self.request.user
        curador_id = self.request.POST.get('curador_pk')
        
        if not curador_id:
            response = {'mensagem': 'Falha. Curador não informado.'}
            return JsonResponse(response)
    
        curador = account_models.User.objects\
            .filter(pk=curador_id)\
            .first()

        if not curador:
            response = {'mensagem': 'Falha. Curador não Cadastrado.'}
            return JsonResponse(response)
    
        has_obj = models.Atendimento\
            .objects\
            .filter(
                curador=curador,
                cliente=user,
            )\
            .first()
        
        if has_obj:
            msg = 'Você já está com uma sessão em aberto com {}. Obrigado.'.format(curador)
            messages.info(request, msg)
            return JsonResponse(response)
            
        contrato = models.Atendimento()
        contrato.curador = curador
        contrato.cliente = user
        try:
            contrato.save()
            msg = 'Olá {}, você e {} firmaram um compromisso. Desejamos sucesso!'\
                .format(user, curador)
            messages.success(request, msg)

            msg = 'Em breve {} entrará em contato, aguarde.'.format(curador)
            messages.info(request, msg)
            
            curador_utils.curador_has_new_cliente(curador, user)
            
        except ValueError as e:
            msg = 'Infelizmente algo saiu errado {}.\n\
                Por favor informe nosso time, obrigado'.format(e)
            messages.warning(request, msg)
            
        return JsonResponse(response)

