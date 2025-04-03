from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView
from produccion_app.models import LoteGalletas, SolicitudProduccion
from . import forms

class ListaSolicitudesProduccionView(ListView):
    model = SolicitudProduccion
    template_name = 'lista_solicitud_produccion.html'
    context_object_name = 'solicitudes'

class CrearSolicitudProduccionView(FormView):
    template_name = 'agregar_solicitud_produccion.html'
    form_class = forms.AgregarSolicitudForm
    success_url = reverse_lazy('lista_solicitudes')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class CreacionProduccionGalletasView(TemplateView):
    template_name = 'produccion_activa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitudes_abiertas'] = SolicitudProduccion.objects.filter(estado='PENDIENTE')
        return context