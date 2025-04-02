from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django import forms
from produccion_app.models import SolicitudProduccion, LoteGalletas

class ListaSolicitudesProduccionView(TemplateView):
    template_name = 'lista_solicitud_produccion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listaProduccion = SolicitudProduccion.objects.all()
        context['listaProduccion'] = listaProduccion
        return context


class CrearProductoView(FormView):
    template_name = 'crear_produccion.html'
    form_class = forms.ProductoRegistrarForm
    success_url = reverse_lazy('lista_solicitudes')

    def form_valid(self,form):
        # Guardar el producto en la base de datos
        form.save()
        return super().form_valid(form)
    
class EditarProductoView(FormView):
    template_name = 'editar_produccion.html'
    form_class = forms.EditarProductoForm
    success_url = reverse_lazy('lista_solicitudes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        producto = get_object_or_404(SolicitudProduccion, id=id)
        kwargs['instance'] = producto
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class CrearSolicitudProduccionView(FormView):
    template_name = 'agregar_solicitud_produccion.html'
    form_class = forms.CrearSolicitudProduccionForm
    success_url = reverse_lazy('lista_solicitudes')

    def form_valid(self, form):
        # Guardar la solicitud de producción en la base de datos
        form.save()
        return super().form_valid(form)
    
