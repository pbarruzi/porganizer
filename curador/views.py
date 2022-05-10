from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import (View, ListView, TemplateView,)
from django.views.generic.edit import (UpdateView)
from django.db import transaction
from django.urls import reverse_lazy


from atendimento import models as atendimento_models
from atendimento.models import ABERTO, ENCERRADO
from account import models as account_models
from curador.forms import EncerrarAtendimentoForm
from curador import utils as curador_utils


class CuradorDashboardView(TemplateView):
    template_name = 'curador/curador-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        atendimentos_correntes = atendimento_models.Atendimento.objects.filter(
            curador=user,
            status_agendamento=ABERTO,
        ).order_by('curador')

        context['atendimentos_correntes'] = atendimentos_correntes
        return context


class CuradorEncerrarAtendimentoView(UpdateView):
    template_name = 'curador/encerrar-atendimento.html'
    success_url = reverse_lazy('curador:dashboard')
    # form_class = EncerrarAtendimentoForm
    model = atendimento_models.Atendimento
    fields = ['anotacoes_curador']

    def form_valid(self, form):
        form.instance.data_encerramento = datetime.now()
        form.instance.status_agendamento = ENCERRADO
        
        anotacoes = form.instance.anotacoes_curador + '  #Encerrado em {}'\
            .format(datetime.now())
        form.instance.anotacoes_curador = anotacoes
        
        msg = 'Contrato entre {} e você está encerrado!'\
            .format(form.instance.cliente)
        messages.success(self.request, msg)

        msg = 'Um email foi enviado ao cliente ( {} ), informando o novo status'\
            .format(form.instance.cliente.email)
        messages.info(self.request, msg)
        
        curador_utils.curador_ended_session(
            form.instance.curador,
            form.instance.cliente)
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        atendimento_id = kwargs.get('pk')
        if atendimento_id:
            atendimento = atendimento_models.Atendimento.objects\
                .filter(pk=atendimento_id)\
                .first()
            context['atendimento'] = atendimento
            
        return context
 

class zCuradorEncerrarAtendimentoView(View):
    template_name = 'curador/encerrar-atendimento.html'
    success_url = reverse_lazy('curador:dashboard')
    form_class = EncerrarAtendimentoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        atendimento_id = kwargs.get('atendimento_id')
        if atendimento_id:
            atendimento = atendimento_models.Atendimento.objects\
                .filter(pk=atendimento_id)\
                .first()
            context['atendimento'] = atendimento_id
            
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = self.request.user
        atendimento_id = kwargs.get('atendimento_id')
        
        if not atendimento_id:
            msg = 'Atendimento não identificado (ID)'
            messages.warning(self.request, msg)
            return HttpResponseRedirect(self.success_url)
    
        contrato = atendimento_models.Atendimento.filter(pk=atendimento_id)
        contrato.data_encerramento = datetime.now()
        contrato.status_agendamento = ENCERRADO
        try:
            contrato.save()
            msg = 'Contrato entre {} e você está encerrado!'\
                .format(contrato.cliente)
            messages.success(request, msg)

            msg = 'Um email foi enviado ao cliente ( {} ), informando o novo status'\
                .format(contrato.cliente.email)
            messages.info(request, msg)
            
            curador_utils.curador_has_ended_session(user, contrato.cliente)
            
        except ValueError as e:
            msg = 'Infelizmente algo saiu errado {}.\n\
                Por favor informe nosso time, obrigado'.format(e)
            messages.warning(request, msg)
        
        return HttpResponseRedirect(self.success_url)


class CuradorPassadoListView(ListView):
    template_name = 'atendimento/cliente-avaliar-curador.html'
    success_url = reverse_lazy('agendamento:cliente-dashboard')
    # form_class = AtendimentoAvalForm
    model = atendimento_models.Atendimento
    fields = ['depoimento_cliente']

    def form_valid(self, form):
        form.instance.data_depoimento = datetime.now()
        form.save()
        return super().form_valid(form)
        
