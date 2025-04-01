
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from . import forms
from produccion_app.models import Produccion


class ProduccionActivaView(View):
    template_name = 'produccion_activa.html'

    def get(self, request):
        producciones = Produccion.objects.filter(estado='en_proceso')
        return render(request, self.template_name, {'producciones': producciones})


class CrearProduccionView(FormView):
    template_name = 'crear_produccion.html'
    form_class = forms.CrearProduccionForm
    success_url = reverse_lazy('produccion_activa')

    def form_valid(self, form):
        produccion = form.save()

        materia_prima = produccion.materia_prima
        materia_prima.cantidad_disponible -= produccion.cantidad_materia_prima_utilizada
        materia_prima.save()
        return super().form_valid(form)


class EditarProduccionView(FormView):
    template_name = 'editar_produccion.html'
    form_class = forms.EditarProduccionForm
    success_url = reverse_lazy('produccion_activa')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        produccion = get_object_or_404(Produccion, id=id)
        kwargs['instance'] = produccion
        return kwargs

    def form_valid(self, form):
        produccion = form.save()
        if produccion.estado == 'finalizado':
            produccion.finalizar_produccion()
        return super().form_valid(form)
