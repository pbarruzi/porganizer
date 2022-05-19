from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import (View, ListView, TemplateView, FormView)
from django.views.generic.edit import (UpdateView)
from django.db import transaction
from django.urls import reverse_lazy


from curador import models
from atendimento import models as atendimento_models
from atendimento.models import ABERTO, ENCERRADO
from account import models as account_models
from curador.forms import EncerrarAtendimentoForm, AboutMeForm
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
 
        
class CuradorHistoricoView(TemplateView):
    template_name = 'curador/curador-historico.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        atendimentos_passados = atendimento_models.Atendimento.objects.filter(
            curador=user,
            status_agendamento=ENCERRADO,
        ).order_by('curador')

        context['atendimentos_passados'] = atendimentos_passados
        return context


class CuradorAboutMeView(UpdateView):
    template_name = 'curador/about-me.html'
    success_url = reverse_lazy('curador:dashboard')
    form_class = AboutMeForm
    model = models.CuradorAboutMe

    def get_object(self):
        user = self.request.user
        about_me_obj = models.CuradorAboutMe\
            .objects\
            .filter(curador=user)\
            .first()
        if not about_me_obj:
            about_me_obj = models.CuradorAboutMe()
            about_me_obj.curador = user
            about_me_obj.save()
        
        return about_me_obj


    def form_valid(self, form):
        curador = self.request.user
        form.instance.curador = curador
        form.save()
        return super().form_valid(form)


class xCuradorAboutMeView(View):
    template_name = 'curador/about-me.html'
    success_url = reverse_lazy('curador:dashboard')
    form_class = AboutMeForm
    model = models.CuradorAboutMe
    fields = ['anotacoes_curador']

    def get_object(self):
        user = self.request.user
        about_me_obj = models.CuradorAboutMe\
            .filter(curador=user)\
            .first()
        if not about_me_obj:
            about_me_obj = models.CuradorAboutMe()
            about_me_obj.curador = user
            about_me_obj.save()
        
        return about_me_obj
            
    def post(self, request, *args, **kwargs):
        _post = super().post(request, *args, **kwargs)

        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.curador = self.request.user
            form.save()
        return _post

    def xform_valid(self, form):
        curador = self.request.user
        form.instance.curador = curador
        form.save()
        return super().form_valid(form)
